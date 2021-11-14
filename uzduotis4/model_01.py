from numpy import loadtxt
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split

dataset = loadtxt("pima-indians-diabetes.data.csv", delimiter=",")
training_data, testing_data = train_test_split(dataset, test_size=0.2, random_state=25)

X = training_data[:, 0:8]
Y = training_data[:, 8]
X_train = testing_data[:, 0:8]
Y_test = testing_data[:, 8]

model = Sequential()

model.add(Dense(20, input_dim=8, activation="relu"))
model.add(Dense(10, activation="relu"))
model.add(Dense(10, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
model.summary()

model.fit(X, Y, epochs=200, batch_size=15)

_, accuracy = model.evaluate(X, Y)
print("Accuracy on training: %.2f" % (accuracy * 100))

_, accuracy = model.evaluate(X_train, Y_test)
print("Accuracy on test: %.2f" % (accuracy * 100))

# Išsaugoti modelį į failą (HDF5 formatas)
model.save("trained_model_01.h5")

# Įkelti modelį iš failo
new_model = load_model("trained_model_01.h5")
new_model.summary()
