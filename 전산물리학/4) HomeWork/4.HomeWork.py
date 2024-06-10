############################################################
# data curing                                              #
############################################################
import os, shutil

#download here : https://www.microsoft.com/en-us/download/details.aspx?id=54765
original_dataset_dir = 'C:\github\Assignment_archive\Data\PetImages'

base_dir = 'C:\github\Assignment_archive\Data\cats_and_dogs_small'
os.mkdir(base_dir)

train_dir = os.path.join(base_dir, 'train')
os.mkdir(train_dir)

validation_dir = os.path.join(base_dir, 'validation')
os.mkdir(validation_dir)

test_dir = os.path.join(base_dir, 'test')
os.mkdir(test_dir)

train_cats_dir = os.path.join(train_dir, 'cats')
os.mkdir(train_cats_dir)

train_dogs_dir = os.path.join(train_dir, 'dogs')
os.mkdir(train_dogs_dir)

validation_cats_dir = os.path.join(validation_dir, 'cats')
os.mkdir(validation_cats_dir)

validation_dogs_dir = os.path.join(validation_dir, 'dogs')
os.mkdir(validation_dogs_dir)

test_cats_dir = os.path.join(test_dir, 'cats')
os.mkdir(test_cats_dir)

test_dogs_dir = os.path.join(test_dir, 'dogs')
os.mkdir(test_dogs_dir)


fnames = ['cat.{}.jpg'.format(i) for i in range(1000)]
for fname in fnames:
    fn1 = fname.replace('cat.','')
    src = os.path.join(original_dataset_dir+"/Cat/", fn1)
    dst = os.path.join(train_cats_dir, fname)
    shutil.copyfile(src, dst)
fnames = ['cat.{}.jpg'.format(i) for i in range(1000, 1500)]
for fname in fnames:
    fn1 = fname.replace('cat.','')
    src = os.path.join(original_dataset_dir+"/Cat/", fn1)
    dst = os.path.join(validation_cats_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['cat.{}.jpg'.format(i) for i in range(1500, 2000)]
for fname in fnames:
    fn1 = fname.replace('cat.','')
    src = os.path.join(original_dataset_dir+"/Cat/", fn1)
    dst = os.path.join(test_cats_dir, fname)
    shutil.copyfile(src, dst)

fnames = ['dog.{}.jpg'.format(i) for i in range(1000)]
for fname in fnames:
    fn1 = fname.replace('dog.','')
    src = os.path.join(original_dataset_dir+"/Dog/", fn1)
    dst = os.path.join(train_dogs_dir, fname)
    shutil.copyfile(src, dst)
    
fnames = ['dog.{}.jpg'.format(i) for i in range(1000, 1500)]
for fname in fnames:
    fn1 = fname.replace('dog.','')
    src = os.path.join(original_dataset_dir+"/Dog/", fn1)
    dst = os.path.join(validation_dogs_dir, fname)
    shutil.copyfile(src, dst)
    
fnames = ['dog.{}.jpg'.format(i) for i in range(1500, 2000)]
for fname in fnames:
    fn1 = fname.replace('dog.','')
    src = os.path.join(original_dataset_dir+"/Dog/", fn1)
    dst = os.path.join(test_dogs_dir, fname)
    shutil.copyfile(src, dst)


print('total training cat images:', len(os.listdir(train_cats_dir)))
print('total training dog images:', len(os.listdir(train_dogs_dir)))
print('total validation cat images:', len(os.listdir(validation_cats_dir)))
print('total validation dog images:', len(os.listdir(validation_dogs_dir)))
print('total test cat images:', len(os.listdir(test_cats_dir)))
print('total test dog images:', len(os.listdir(test_dogs_dir)))

#############################################################
#augmentation                                              #
#############################################################

import os
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

# 베이스 디렉토리 설정
base_dir = r'C:\github\Assignment_archive\Data\cats_and_dogs_small'
train_dir = os.path.join(base_dir, 'train')

# 고양이와 개 이미지 경로 설정
train_cats_dir = os.path.join(train_dir, 'cats')
train_dogs_dir = os.path.join(train_dir, 'dogs')

# 이미지 데이터 증강 설정
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# 531번째 고양이와 개 이미지 파일 선택
cat_fnames = sorted([os.path.join(train_cats_dir, fname) for fname in os.listdir(train_cats_dir) if fname.lower().endswith(('.png', '.jpg', '.jpeg'))])
dog_fnames = sorted([os.path.join(train_dogs_dir, fname) for fname in os.listdir(train_dogs_dir) if fname.lower().endswith(('.png', '.jpg', '.jpeg'))])

# 인덱스가 유효한지 확인
if len(cat_fnames) > 530 and len(dog_fnames) > 530:
    cat_img_path = cat_fnames[530- 49] 
    dog_img_path = dog_fnames[530- 49] 
else:
    raise ValueError("531번째 이미지를 찾을 수 없습니다. 이미지 파일이 충분하지 않습니다.")

# 이미지를 로드하고 배열로 변환
def load_and_process_image(img_path):
    img = load_img(img_path, target_size=(150, 150))
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
    return x

cat_img_array = load_and_process_image(cat_img_path)
dog_img_array = load_and_process_image(dog_img_path)

# 증강 이미지 시각화 함수
def plot_augmented_images(img_array, title):
    i = 0
    plt.figure(figsize=(20, 4))
    for batch in datagen.flow(img_array, batch_size=1):
        plt.subplot(2, 5, i + 1)
        imgplot = plt.imshow(batch[0].astype('uint8'))
        plt.axis('off')
        i += 1
        if i % 10 == 0:
            break
    plt.suptitle(title)
    plt.show()

# 10개의 증강된 이미지 시각화
plot_augmented_images(cat_img_array, 'Augmented Cat Images')
plot_augmented_images(dog_img_array, 'Augmented Dog Images')

#############################################################
# IMDB Dataset: Sentiment Analysis                          #
#############################################################

from keras.datasets import imdb

(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)

print(train_data[0])
print(train_labels[0])

word_index = imdb.get_word_index()

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])

decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])

print(decoded_review)

import numpy as np

def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(partial_x_train,
                    partial_y_train, 
                    epochs=20,
                    batch_size=512,
                    validation_data=(x_val, y_val))

import matplotlib.pyplot as plt
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(loss) + 1)

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()

############################################################
# Reuters                                                  #
############################################################

from keras.datasets import reuters

(train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words=10000)

print(train_data[0])
print(train_labels[0])

word_index = reuters.get_word_index()
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in train_data[0]])

print(decoded_review)

import numpy as np


def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

def to_one_hot(labels, dimension=46):
    results = np.zeros((len(labels), dimension))
    for i, label in enumerate(labels):
        results[i, label] = 1.
    return results

from keras.utils.np_utils import to_categorical
one_hot_train_labs = to_categorical(train_labels)
one_hot_test_labs  = to_categorical(test_labels)

from keras import models
from keras import layers

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(46, activation='sigmoid'))

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train,
          one_hot_train_labs, 
          epochs=20,
          batch_size=512,
          )   

results = model.evaluate(x_test,one_hot_test_labs)

print ("Final Results = ", results)

#################################################################
#Boston Housing                                                 #
#################################################################

from keras.datasets import boston_housing

(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()
print("TR shape : ", train_data.shape)
print("TE shape : ", test_data.shape)

print("TR target shape : ", train_targets.shape)
print("TE target shape : ",test_targets.shape)

acronyms    = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE',
                'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
definitions = ['per capita crime rate', 
               'proportion of residential land zoned for lots over 25,000 sq.ft.',
               'proportion of non-retail business acres per town',
               'Charles River dymmy variable (=1 if tract bounds river; 0 otherwise)',
               'nitric oxides concentration (parts per 10 million)',
               'The average number of rooms per dwelling',
               'The proportion of owner-occupied units built prior to 1940',
               'weighted distances to five Boston employment centers',
               'full-value property-tax rate per $10,000',
               'pupil-teacher ratio by town',
               '1000*(Bk-0.63)**2 where Bk is the proportion of blacks by town',
               'percentage lower status of the population']

crim = []
zn   = []
tget = []

mean = train_data.mean(axis=0)
print(mean)

train_data -= mean
std = train_data.std(axis=0)
train_data /= std

test_data -= mean
test_data /= std

import numpy as np

for i in range(len(train_data)):
    crim.append(train_data[i][0])
    zn.append(train_data[i][1])
    tget.append(train_data[i][2])

y, binEdges = np.histogram(crim, bins = 100)
bincenters = 0.5 * (binEdges[1:]+binEdges[:-1])
width = 0.0099

import matplotlib.pyplot as plt
plt.bar(bincenters, y, width)
plt.show()

#################################################################
#Boston Housing : DNN wirh dropout                              #
#################################################################

from keras.datasets import boston_housing

(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()

print("data = ", train_data)

mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std

test_data -= mean
test_data /= std

from keras import models
from keras import layers

def build_model():
    model = models.Sequential()
    model.add(layers.Dense(64, activation='relu',input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(1)) # no activation to not have constraints
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    return model

import numpy as np
model = build_model()
model.fit(train_data, train_targets, epochs=100, batch_size=1)
test_mse_score, test_mae_score = model.evaluate(test_data, test_targets)

print(test_mae_score)

predictions = model.predict(test_data)

Diff = []

for i in range(102) :
    percentdiff = (test_targets[i] - predictions[i][0])/test_targets[i] * 100.0
    Diff.append(percentdiff)

y, binEdges = np.histogram(Diff, bins = 50)
bincenters = 0.5 * (binEdges[1:]+binEdges[:-1])
import matplotlib.pyplot as plt
plt.bar(bincenters, y)
plt.show()