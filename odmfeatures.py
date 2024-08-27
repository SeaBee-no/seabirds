from numpy import load

data = load('C:/Users/sindre.molvarsmyr/Downloads/DJI_20230628125219_0002_D.JPG.features.npz')
lst = data.files
for item in lst:
    print(item)
    print(data[item])


