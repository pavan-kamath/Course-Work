import tensorflow as tf
import tensorflow.keras
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications import imagenet_utils
from tensorflow.keras.layers import Dense,GlobalAveragePooling2D
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications.mobilenet import preprocess_input
import numpy as np
from IPython.display import Image
from tensorflow.keras.optimizers import Adam
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from sklearn.metrics import confusion_matrix, classification_report,ConfusionMatrixDisplay, classification_report

def prepare_image(file):
    img_path = ''
    img = image.load_img(img_path + file, target_size=(1920,1080))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tensorflow.keras.applications.{model_name}.preprocess_input(img_array_expanded_dims) ##changing the model name as needed for multimodel comparison
##model_name used: MobileNet,ResNet50,ResNet152,InceptionV3

def load_image(img_path, show=False):
    img = image.load_img(img_path, target_size=(1920, 1080))
    img_tensor = image.img_to_array(img)                    # (height, width, channels)
    img_tensor = np.expand_dims(img_tensor, axis=0)         # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor /= 255.                                      # imshow expects values in the range [0, 1]
    if show:
        plt.imshow(img_tensor[0])                           
        plt.axis('off')
        plt.show()

    return img_tensor

#define the base model   
base_model = tf.keras.applications.{model_name}(weights = 'imagenet', include_top = False, input_shape = (1920,1080,3)) ##changing the model name as needed for multimodel comparison

x=base_model.output
x=GlobalAveragePooling2D()(x)
x=Dense(1024,activation='relu')(x) #we add dense layers so that the model can learn more complex functions and classify for better results.
x=Dense(1024,activation='relu')(x) #dense layer 2
x=Dense(512,activation='relu')(x) #dense layer 3
x = Dense(1000, activation='relu')(x)
preds = Dense(4, activation = 'softmax')(x)
model=Model(inputs=base_model.input,outputs=preds)
model.compile(optimizer='Adam',loss='categorical_crossentropy',metrics=['accuracy']) # Adam optimizer, loss function will be categorical cross entropy, evaluation metric will be accuracy

for layer in base_model.layers:
    layer.trainable = False
    
#using the inbuilt function to read the train and test images
train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input) #included in our dependencies

train_generator=train_datagen.flow_from_directory('/home/kiran/mece/train',
                                                 target_size=(1920,1080),
                                                 color_mode='rgb',
                                                 batch_size=2,
                                                 class_mode='categorical',
                                                 shuffle=True)


step_size_train=train_generator.n//train_generator.batch_size
history = model.fit_generator(generator=train_generator,
                   steps_per_epoch=step_size_train,
                   epochs=10)
                   
test_generator=train_datagen.flow_from_directory('/home/kiran/mece/test',
                                                 target_size=(1920,1080),
                                                 color_mode='rgb',
                                                 batch_size=2,
                                                 class_mode='categorical',
                                                 shuffle=True)

evaluate = model.evaluate_generator(generator=test_generator)

#plotting the resulsts
fig, axs = plt.subplots(2, 1, figsize=(15,15))
axs[0].plot(history.history['loss'])
axs[0].plot(history.history['val_loss'])
axs[0].title.set_text('Training Loss vs Validation Loss')
axs[0].set_xlabel('Epochs')
axs[0].set_ylabel('Loss')
axs[0].legend(['Train','Val'])
axs[1].plot(history.history['accuracy'])
axs[1].plot(history.history['val_accuracy'])
axs[1].title.set_text('Training Accuracy vs Validation Accuracy')
axs[1].set_xlabel('Epochs')
axs[1].set_ylabel('Accuracy')
axs[1].legend(['Train', 'Val'])

#testing to see if the prediction works
img_path = 'img23.png'
new_image = load_image(img_path,show=True)
pred = model.predict(new_image)
pred.argmax()

#predicting the class for all test images
y_pred = []
for i in tqdm(test_generator):
    pred = model.predict(i[0])
    label = np.argmax(pred)
    y_pred.append(label)
    
y_pred_4000 = y_pred[:4000] #for some reason, the predictor was running beyond the test generator max index. Cutting it down to first 4000 values

#confusion matrix
cm = confusion_matrix(test_generator.labels, y_pred_4000 )
disp = ConfusionMatrixDisplay(cm)
disp.plot()
plt.show()