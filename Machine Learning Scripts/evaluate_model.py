from keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Load the model
model = load_model('./models/currency_classifier_resnet50.h5')

# Define the data generator for test data
test_datagen = ImageDataGenerator(rescale=1.0/255)

# Create the test generator
test_generator = test_datagen.flow_from_directory('../datasets/valid',
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    shuffle=False
)

# Evaluate the model
test_loss, test_acc = model.evaluate(test_generator)
print(f'Test Loss: {test_loss}')
print(f'Test Accuracy: {test_acc}')

# Optional: Print confusion matrix and classification report
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report

# Get true labels and predictions
test_generator.reset()
Y_pred = model.predict(test_generator)
y_pred = np.argmax(Y_pred, axis=1)
y_true = test_generator.classes

# Print confusion matrix
cm = confusion_matrix(y_true, y_pred)
print("Confusion Matrix:")
print(cm)

# Print classification report
print("Classification Report:")
print(classification_report(y_true, y_pred, target_names=test_generator.class_indices.keys()))
