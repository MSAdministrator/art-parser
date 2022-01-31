import typing
import attr


@attr.s
class AtomicTestInput:

    name: typing.AnyStr        = attr.ib()
    description: typing.AnyStr = attr.ib()
    type: typing.AnyStr        = attr.ib()
    default: typing.AnyStr     = attr.ib()

    @type.validator
    def check(self, attribute, value):
        if isinstance(value, str) and value.capitalize() not in ['Path', 'path', 'Url', 'String', 'string', 'Integer', 'Float']:
            raise ValueError(f"{attribute} must be one of 'Path', 'Url', 'String', 'Integer', 'Float' not {value}")


@attr.s
class AtomicExecutor:

    name: typing.AnyStr                     = attr.ib()
    command: typing.AnyStr                  = attr.ib()
    cleanup_command: typing.AnyStr          = attr.ib(default=None)
    elevation_required: typing.AnyStr       = attr.ib(default=False)
    steps: typing.AnyStr                    = attr.ib(default=None)


@attr.s
class AtomicDependency:

    description: typing.AnyStr = attr.ib()
    get_prereq_command: typing.AnyStr = attr.ib(default=None)
    prereq_command: typing.AnyStr = attr.ib(default=None)


@attr.s
class AtomicTest:
    """A single Atomic test object structure

    Returns:
        AtomicTest: A single Atomic test object
    """

    name: typing.AnyStr                                        = attr.ib()
    description: typing.AnyStr                                 = attr.ib()
    supported_platforms: typing.List                           = attr.ib()
    auto_generated_guid: typing.AnyStr                         = attr.ib()
    executor: typing.AnyStr                                    = attr.ib()
    input_arguments: typing.List[AtomicTestInput]              = attr.ib(default=None)
    dependency_executor_name: typing.AnyStr                    = attr.ib(default=None)
    dependencies: typing.List[AtomicDependency]                = attr.ib(default=[])

    def __attrs_post_init__(self):
        if self.input_arguments:
            temp_list = []
            for key,val in self.input_arguments.items():
                argument_dict = {}
                argument_dict = val
                argument_dict.update({'name': key})
                temp_list.append(AtomicTestInput(**argument_dict))
            self.input_arguments = temp_list
        if self.executor:
            executor_dict = self.executor
            if executor_dict.get('name') == 'manual':
                if not executor_dict.get('command'):
                    executor_dict['command'] = ''
            self.executor = AtomicExecutor(**executor_dict)
            executor_dict = None
        else:
            self.executor = []
        if self.dependencies:
            dependency_list = []
            for dependency in self.dependencies:
                dependency_list.append(AtomicDependency(**dependency))
            self.dependencies = dependency_list

    @supported_platforms.validator
    def check(self, attribute, value):
        if isinstance(value, list):
            for item in value: 
                if item not in ["windows","macos","linux","office-365","azure-ad","google-workspace","saas","iaas","containers","iaas:gcp","iaas:azure","iaas:aws"]:
                    raise ValueError(f'{attribute} must be one of "windows","macos","linux","office-365","azure-ad","google-workspace","saas","iaas","containers","iaas:gcp","iaas:azure","iaas:aws"')

    @executor.validator
    @dependency_executor_name.validator
    def check_executor(self, attribute, value):
        if isinstance(value, str) and value not in ['command_prompt', 'powershell', 'sh', 'bash', 'manaul', 'gcloud']:
            raise ValueError(f"{attribute} must be one of 'command_prompt', 'powershell', 'sh', 'bash', 'manaul' not {value}")
