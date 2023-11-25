from typing import Optional, List, Annotated
from fastapi import FastAPI, Path, Query, Depends, APIRouter, HTTPException
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/question/")
async def generate_paper(total:int, easy:int, med:int, hard:int, db:db_dependency):
    try:
        easy_ques = db.query(models.questions).filter(models.questions.difficulty == 'Easy').all()
        med_ques = db.query(models.questions).filter(models.questions.difficulty == 'Medium').all()
        hard_ques = db.query(models.questions).filter(models.questions.difficulty == 'Hard').all()
        easy = (total*easy)//100
        med = (total*med)//100
        hard = (total*hard)//100
        print(easy,med,hard)
        d = {'easy':set(), 'med':set(), 'hard':set()}
        
        #Recursive function to choose questions from the database
        #accroding to the given constraints
        def get_questions(ques_set,diff,total,visited):
            if total == 0:
                for q in visited:d[diff].add(q)
            for ques in ques_set:
                if ques not in visited and ques.marks <= total:
                    visited.add(ques)
                    possible = get_questions(ques_set,diff,total-ques.marks,visited)
                    if possible:return possible
                    visited.remove(ques)
        
        #getting question of each difficulty
        get_questions(easy_ques,'easy',easy,set())
        get_questions(med_ques,'med',med,set())
        get_questions(hard_ques,'hard',hard,set())

        #checking if the given question combination is valid or not
        if (d['easy'] == set() and easy > 0) or (d['med'] == set()  and med > 0) or (d['hard'] == set() and hard > 0):
            raise HTTPException(status_code=404, detail='Invalid combination of questions')
        
        #returning the question paper
        return list(d['easy'])+list(d['med'])+list(d['hard'])
    except:
        raise HTTPException(status_code=404, detail='Oops something went wrong')