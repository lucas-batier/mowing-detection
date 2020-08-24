import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, activations, metrics
from tensorflow.keras.models import Model, Sequential
from tensorflow.math import confusion_matrix
import numpy as np
from sklearn.model_selection import train_test_split, KFold, StratifiedKFold
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
import sys
import argparse

parser=argparse.ArgumentParser(
    description='''Create and save the modal dataset (Sentinel images)''')
parser.add_argument('-m','--mode', help='Modal dataset path', required=True)
parser.add_argument('-c','--context', help='Contextual dataset path', required=True)
parser.add_argument('-l','--labels', help='Labels vector path', required=True)
args=parser.parse_args()

mode = np.load(args.mode)
context = np.load(args.context)
labels = np.load(args.labels)

labels = labels.astype('uint8')
labels = np.reshape(labels, (labels.shape[0], 1, 1))

mode_tr, mode_te, context_tr, context_te, labels_tr, labels_te = train_test_split(mode, context, labels, test_size=0.2)

print()
print('%.2f %% of mowed parcels'%(np.sum(labels)/len(labels)*100))
print()

def layers_Normalization(inputs):
    return tf.clip_by_value(tf.divide(tf.subtract(inputs, tf.reduce_min(inputs)), tf.subtract(tf.reduce_max(inputs), tf.reduce_min(inputs))), -1e12, 1e12) # Normalization

def model_creation_context():
    keras.backend.clear_session()
    
    # MLP modal encoding
    mode_input = keras.Input(shape=(mode.shape[1], mode.shape[2]))
    mode_encoded = layers.TimeDistributed(layers.Dense(36))(mode_input)
    mode_encoded = layers.TimeDistributed(layers.Activation('relu'))(mode_encoded)
    mode_encoded = layers.TimeDistributed(layers.Dropout(0.2))(mode_encoded)
    #mode_encoded = mode_input

    # MLP context encoding
    cont_input = keras.Input(shape=(context.shape[1], context.shape[2]))
    cont_encoded = cont_input

    # Concatenate
    encoded = layers.concatenate([mode_encoded, cont_encoded])
    #encoded = mode_encoded
    
    # RNN
    rnn = layers_Normalization(encoded)
    rnn = layers.GRU(rnn.shape[2], return_sequences=True)(rnn)

    # MLP predicting
    decoded = layers.Dense(1)(rnn)
    decoded = layers.Permute((2, 1))(decoded)

    # MLP time predicting
    outputs = layers.TimeDistributed(layers.Dense(5))(decoded)
    outputs = layers.Activation('relu')(outputs)
    outputs = layers.Dropout(0.2)(outputs)
    outputs = layers.TimeDistributed(layers.Dense(1))(outputs)
    outputs = layers_Normalization(outputs)


    # Compilation
    model = Model(inputs=[mode_input, cont_input], outputs=outputs)
    model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.01), loss='mean_squared_error')
    
    return model

def model_creation_nocontext():
    keras.backend.clear_session()
    
    # MLP modal encoding
    mode_input = keras.Input(shape=(mode.shape[1], mode.shape[2]))
    mode_encoded = layers.TimeDistributed(layers.Dense(36))(mode_input)
    mode_encoded = layers.TimeDistributed(layers.Activation('relu'))(mode_encoded)
    mode_encoded = layers.TimeDistributed(layers.Dropout(0.2))(mode_encoded)
    mode_encoded = mode_input

    # MLP context encoding
    cont_input = keras.Input(shape=(context.shape[1], context.shape[2]))
    cont_encoded = cont_input

    # Concatenate
    encoded = layers.concatenate([mode_encoded, cont_encoded])
    #encoded = mode_encoded
    
    # RNN
    rnn = layers_Normalization(encoded)
    rnn = layers.GRU(rnn.shape[2], return_sequences=True)(rnn)

    # MLP predicting
    decoded = layers.Dense(1)(rnn)
    decoded = layers.Permute((2, 1))(decoded)

    # MLP time predicting
    outputs = layers.TimeDistributed(layers.Dense(5))(decoded)
    outputs = layers.Activation('relu')(outputs)
    outputs = layers.Dropout(0.2)(outputs)
    outputs = layers.TimeDistributed(layers.Dense(1))(outputs)
    outputs = layers_Normalization(outputs)


    # Compilation
    model = Model(inputs=[mode_input, cont_input], outputs=outputs)
    model.compile(optimizer=keras.optimizers.SGD(learning_rate=0.01), loss='mean_squared_error')
    
    return model

print()
print('Training')
print()

history = []
auc = []
K = 5
kf = StratifiedKFold(n_splits=K)
k = 0
for tr_ind, te_ind in kf.split(mode, labels[:,:,0]):
    k += 1
    print('Fold n°%d'%(k))
    # Train test split
    mode_train, mode_test = mode[tr_ind], mode[te_ind]
    cont_train, cont_test = context[tr_ind], context[te_ind]
    labels_train, labels_test = labels[tr_ind], labels[te_ind]
    # Learning
    model = model_creation_context()
    history.append(model.fit([mode_train, cont_train], labels_train, epochs=10, verbose=1))
    # Testing
    pred = model.predict([mode_test, cont_test])[:,:,0][:,0].astype('uint8')
    true = labels_test.astype('uint8')[:,:,0]
    
    auc.append(roc_auc_score(true, pred))

print()
print('Testing')
print()

k = 0
for score in auc:
    k += 1
    print('Fold n°%d'%(k))
    print('AUC = %.3f'%(roc_auc_score(true, pred)))
