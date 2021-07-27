from interface.read_out import read_out

read_out.init()
read_out.connect()
cd_d, ndc = read_out.get_data()

print(cd_d)
print(ndc)

read_out.close()