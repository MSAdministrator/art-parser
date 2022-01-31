import typing
from .atomictest import AtomicTest
from pyattck import Attck
import attr


@attr.s
class Atomic:
    """A single Atomic data structure. Each Atomic (technique)
    will contain a list of one or more AtomicTest objects.
    """

    attack_technique: typing.AnyStr                      = attr.ib()
    display_name: typing.AnyStr           = attr.ib()
    atomic_tests: typing.List[AtomicTest] = attr.ib()
    mitre_description: typing.AnyStr      = attr.ib(default=None)
    mitre_technique_name: typing.AnyStr   = attr.ib(default=None)
    tactic_name: typing.AnyStr            = attr.ib(default=None)
    tactic_id: typing.AnyStr              = attr.ib(default=None)
    platforms: typing.List                = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.atomic_tests:
            test_list = []
            for test in self.atomic_tests:
                test_list.append(AtomicTest(**test))
            self.atomic_tests = test_list
        attck = Attck(nested_subtechniques=False)
        if self.attack_technique:
            for technique in attck.enterprise.techniques:
                if technique.id == self.attack_technique:
                    self.mitre_description = technique.description
