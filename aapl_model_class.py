# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 23:15:31 2022

@author: Jaspreet Singh
"""
from pydantic import BaseModel

# Class for Input in Model
class Newz_Senti(BaseModel):
    Newz_Headline: str
    