import sqlite3

class SQL_bot:
    def __init__(self):
        self.data = sqlite3.connect('data.db')

    def get_subscriptions(self):
        '''get all subscriptions'''
        command = 'SELECT user_id FROM Users WHERE status=1'
        with self.data :
            res = self.data.execute(command)
        out = []
        for i in res:
            out.append(i[0])
        return out


    def subscribe(self ,user_id ,un = False):
        '''add user into db(or change status if user was exist earlier) or change user status to 0 in DB and remove from user_id list'''
        exist = self.user_exist_id(user_id)

        if un==False:
            if exist:
                command = 'UPDATE Users SET status = 1 WHERE user_id={}'.format(user_id)
            else:
                with self.data:
                    last_id = list(self.data.execute('SELECT max(id) FROM Users'))[0][0]
                    last_id = 0 if last_id == None else last_id

                command = 'INSERT INTO Users VALUES({0},{1},{2})'.format(last_id+1,user_id,1)
        else:
            if exist:
                command = 'UPDATE Users SET status = 0 WHERE user_id={}'.format(user_id)

        with self.data:
            self.data.execute(command)

    def user_exist_id(self , user_id):
        '''returns id if user exist otherwise False'''
        with self.data:
            command = 'SELECT id FROM Users where user_id = {}'.format(user_id)
            user = list(self.data.execute(command))

        if user :
            return user[0][0]

        return False

    def user_subscribed(self , user_id):
        '''returns status of user(subscripted/ not subscripted)'''
        with self.data:
            command = 'SELECT status FROM Users WHERE user_id = {}'.format(user_id)
            status = list(self.data.execute(command))
        try:
            return status[0][0]
        except Exception:
            return False


    def close(self):
        self.data.close()







if __name__=='__main__':
     x =SQL_bot()
     x.close()

