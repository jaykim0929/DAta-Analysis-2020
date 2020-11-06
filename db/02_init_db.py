import json
import pymysql

with open('mysql.json', 'r') as file:
    config_str = file.read()
config = json.loads(config_str)

conn = pymysql.connect(
    host = config['host'],
    user = config['user'],
    password = config['password'],
    database = config['database'],
    port = config['port']
)

sqlUsers = """
    create table if not exists users (
        uid varchar(20) not null primary key,
        pwd char(44) not null,
        uname varchar(20) not null,
        tel varchar(20),
        email varchar(40),
        regDate datetime default current_timestamp,
        isDeleted int default 0,
        photo varchar(80)
    );
"""
sqlBbs = """
    create table if not exists bbs (
        bid int not null primary key auto_increment,
        uid varchar(20) not null,
        title varchar(100) not null,
        content varchar(4000),
        modTime datetime default current_timestamp,
        viewCount int default 0,
        isDeleted int default 0,
        replyCount int default 0,
        foreign key(uid) references users(uid)
    ) auto_increment=1001;
"""
sqlReplyBbs = """
    create table if not exists reply (
        rid int not null primary key auto_increment,
        bid int not null,
        uid varchar(20) not null,
        content varchar(2000),
        regTime datetime default current_timestamp,
        isMine int default 0,
        foreign key(bid) references bbs(bid),
        foreign key(uid) references users(uid)
    );
"""
users = [
    ('admin', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', '관리자', '010-2345-6789', 'admin@gmail.com', '/upload/blank.png'),
    ('jaykim0929', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', '김광섭', '010-7440-1486', 'jaykim0929@gmail.com', '/upload/blank.png'),
    ('panama1', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', '에스메랄다농장', '010-4679-4679', 'esmelardafarm@gmail.com', '/upload/blank.png'),
    ('kenya', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', 'AA', '010-4646-4646', 'kenyaAB@gmail.com', '/upload/blank.png'),
    ('panama2', 'A6xnQhbz4Vx2HuGl4lXwZ5U2I8iziLRFnhP5eNfIRvQ=', 'hartmann농장', '010-7913-7913', 'hartmann@gmail.com', '/upload/blank.png'),
]
sqlRegister = 'insert into users(uid, pwd, uname, tel, email, photo) values((%s,%s,%s,%s,%s,%s);'
bbsList = [
    ('admin', '커핑노트작성', '각 지역 농장의 커핑 노트 작성을 부탁드립니다.'),
    ('jaykim0929', '추출법 소개', '도구별 추출법 리플로 남겨주세요.'),
    ('panama1', '에스메랄다 게이샤 커핑노트 입니다', 'flower, jasmin, fruits candy, orange, cherry, caramel, vanilla sylup, good valance, deepcreamy body, complexity taste and flaver, long after taste.'),
    ('kenya', '케냐 AA TOP kirinyaga kiangoi 커핑노트 입니다', 'Process: Washed, Cup note: orange, apricot, blueberry, complex, grapefruit, passionfruit'),
    ('panama2', '핀카 하트맨 게이샤 커핑노트 입니다', 'grade : private collection, process: netural, Cup note: jasmin, orange, mango, strawberry, vanilla complex'),
]
sqlInsert = 'insert into bbs(uid, title, content) values(%s, %s, %s);'
replyList = [
    (1005, 'djy', '좋습니다. 매우 훌륭한 작품입니다.'),
    (1005, 'gdhong', '매우매우 훌륭합니다.'),
    (1006, 'eskim', '너무 좋은 작품입니다. 잘 보았어요.')
]
sqlInsertReply = 'insert into reply(bid, uid, content) values(%s, %s, %s);'
bbsReplyList = [
    (1, 1, 1006), (2, 2, 1005)
]
sqlReplyUpdate = 'update bbs set viewCount=%s, replyCount=%s where bid=%s;'

cur = conn.cursor()
cur.execute(sqlUsers)
conn.commit()
cur.executemany(sqlRegister, users)
conn.commit()

cur = conn.cursor()
cur.execute(sqlBbs)
conn.commit()
cur.executemany(sqlInsert, bbsList)
conn.commit()

cur = conn.cursor()
cur.execute(sqlReplyBbs)
conn.commit()
cur.executemany(sqlInsertReply, replyList)
conn.commit()
cur.executemany(sqlReplyUpdate, bbsReplyList)
conn.commit()

cur.close()
conn.close()