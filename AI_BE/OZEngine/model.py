from .dress_checkers import FullDressUniformChecker, NavyServiceUniformChecker
from .dress_classifier import classificate
from .edge_detectors import HED, Morph, RCF
from .person_detectors import haarcascade


class OmilZomil:
    def __init__(self):
        # self.HED_engine = HED()
        print('init!')
        self.org = None
        self.gray = None
        self.edge = None

        self.full_dress_uniform_checker = FullDressUniformChecker()
        self.navy_service_uniform_checker = NavyServiceUniformChecker()

        self.kind = None

    def detect(self, img):
        self.org = img
        # check_person(self.org) # 사람인식
        # hair_ segmentation(org) 머리카락인식
        # kind = classificate(self.org) # 복장종류인식 (전투복, 동정복, 샘당)
        self.kind = '1'
        if self.kind == '1':
            self.navy_service_uniform_checker.checkUniform(self.org)
        elif self.kind == '2':
            self.full_dress_uniform_checker.checkUniform(self.org)

        return None
