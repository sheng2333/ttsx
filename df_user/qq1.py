from itsdangerous import TimedJSONWebSignatureSerializer as tms

# jm=tms('laowang',30)
#
# ret= jm.dumps({'name':'laowang'})
# ret1=jm.loads(ret)
#
# print(ret)
# print(ret1)

# from fdfs_client.client import Fdfs_client
#
# client = Fdfs_client('/etc/fdfs/client.conf')
# ret = client.upload_by_filename('/home/sheng/as.png')
# print(ret)


a=[[[0.1],[0.2]],[[1.1],[1.2]]]

for i in a:
    print(i)
    for j in i:
        print(j)