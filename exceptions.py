####################
# 
# Galina Bovykina
# November 16 2022
#
# This is referenced to create and raise impossible actions
# Code adopted from TStand90 rogueliketutorials.com
#
####################


class Impossible(Exception):
    """raises problems"""


class QuitWithoutSaving(SystemExit):
    """exits script"""
