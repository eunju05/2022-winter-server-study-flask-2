from distutils.util import execute
from pickle import TRUE
from attr import field
from colorama import Cursor
from flask import Flask, request
from flask_restx import Resource, Namespace, abort
from database.database import Database

user = Namespace('user')

@user.route('')
class UserManagement(Resource):
    @user.doc(responses={400: '해당 유저가 존재하지 않음 or 아이디나 비밀번호 불일치'})
    def get(self):
        # GET method 구현 부분
        """유저 데이터 조회"""
        database = Database()
        params = request.get_json()
        id = params['id']
        password = params['password']
        result = {}

        sql = f"SELECT * FROM user WHERE id = '{id}' AND pw = '{password}';"
        result = database.execute_one(sql)
        
        database.commit()
        database.close()
        
        #일치하는 id, pw 없는 경우
        if not result:
            abort(400, "아이디나 비밀번호 불일치")

        #일치하는 id, pw 존재
        else :
            return {
                "nickname": result['nickname']
            }, 200
    
    
    @user.doc(responses={200: '유저 생성 성공'})
    @user.doc(responses={400: '이미 있는 유저'})
    def post(self):
        # POST method 구현 부분
        """유저 생성"""
        database = Database()
        params = request.get_json()
        id = params['id']
        password = params['password']
        nickname = params['nickname']
        dup_check = {}
        
        sql = f"SELECT * FROM user WHERE id = '{id}';"
        dup_check = database.execute_one(sql)

        #유저 생성 가능
        if not dup_check:
            sql = f"INSERT INTO user VALUES('{id}', '{password}', '{nickname}');"
            database.execute(sql)

            database.commit()
            database.close()
            return {
                "is_success": True,
                "message": "유저 생성 성공",
            }, 200
        
        #중복 id 존재, 유저 생성 불가
        else:
            database.commit()
            database.close()
            return {
                "is_success": False,
                "message": "이미 있는 유저",
            }, 400


    @user.doc(responses={200: '유저 닉네임 변경 성공'})
    @user.doc(responses={400: '아이디나 비밀번호 불일치 or 현재 닉네임과 같음'})
    def put(self):
        # PUT method 구현 부분
        """유저 데이터(닉네임) 수정"""
        database = Database()
        params = request.get_json()
        id = params['id']
        password = params['password']
        nickname = params['nickname']
        dup_check = {}
        
        sql = f"SELECT * FROM user WHERE id = '{id}' AND pw = '{password}';"
        dup_check = database.execute_one(sql)

        #일치하는 id, pw 없는 경우
        if not dup_check:
            database.commit()
            database.close()
            return {
                "is_success": False, 
                "message": "아이디나 비밀번호 불일치"
            }, 400

        #일치하는 id, pw 존재
        else:
            #nickname이 같은 경우                       
            if dup_check['nickname'] == nickname:
                database.commit()
                database.close()
                return {
                "is_success": False, 
                "message": "현재 닉네임과 같음"
            }, 400

            #nickname 변경 가능
            else:
                sql = f"UPDATE user SET nickname = '{nickname}' WHERE id = '{id}' AND pw = '{password}';"
                database.execute(sql)
                
                database.commit()
                database.close()
                return {
                    "is_success": True, 
                    "message": "유저 닉네임 변경 성공"
                }
    

    @user.doc(responses={200: '유저 삭제 성공'})
    @user.doc(responses={400: '아이디나 비밀번호 불일치'})
    def delete(self):
        # DELETE method 구현 부분
        """유저 삭제"""
        database = Database()
        params = request.get_json()
        id = params['id']
        password = params['password']
        dup_check = {}
        
        sql = f"SELECT * FROM user WHERE id = '{id}' AND pw = '{password}';"
        dup_check = database.execute_one(sql)

        #일치하는 id, pw 없는 경우
        if not dup_check:
            database.commit()
            database.close()
            return {
                'is_success': False, 
                'message': '아이디나 비밀번호 불일치'
            }, 400

        #일치하는 id, pw 존재
        else:
            sql = f"DELETE FROM user WHERE id = '{id}' AND pw = '{password}';"
            database.execute(sql)

            database.commit()
            database.close()

            return {
                "is_success": True,
                "message": "유저 삭제 성공",
            }, 200