# -*- coding: utf-8 -*-


class User:
    def __init__(self, userId, name, rank, status, channel, auth=False):
        self.userId = userId
        self.name = name
        self.rank = rank
        self.status = status
        self.channel = channel
        self.authenticated = auth

    def __repr__(self):
        r = {
            'user_id': self.userId,
            'name': self.name,
            'rank': self.rank,
            'status': self.status,
            'channel': self.channel,
            'authenticated': self.authenticated,
        }
        return None

    def is_authenticated(self):
        '''user객체가 인증되었다면 True를 반환'''
        return self.authenticated

    def is_active(self):
        '''특정 계정의 활성화 여부, inactive 계정의 경우 로그인이 되지 않도록 설정할 수 있다.'''
        return True

    def is_anonymous(self):
        '''익명의 사용자로 로그인 할 때만 True반환'''
        return False

    def get_id(self):
        '''
        - 사용자의 ID를 unicode로 반환
        - user_loader 콜백 메소드에서 사용자 ID를 얻을 때 사용할 수도 있다.
        '''
        return self.userId



