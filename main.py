#!/usr/bin/env python3

import numpy as np
import tensorflow as tf
import random
import rubiks_cube


def main():
    session = tf.InteractiveSession()

    EMBEDDINGS_DIMENSION = 10
    EMBEDDINGS_SHAPE = [len(rubiks_cube.Color), EMBEDDINGS_DIMENSION]
    embeddings = tf.Variable(tf.truncated_normal(EMBEDDINGS_SHAPE, stddev=0.1))

    x = tf.placeholder(tf.int32, shape=[None, 54])
    e = embed(embeddings, x)

    w0 = tf.Variable(tf.truncated_normal([540, 2048], stddev=0.1))
    b0 = tf.Variable(tf.ones([2048]))

    h0 = tf.nn.relu(tf.matmul(e, w0) + b0)

    w1 = tf.Variable(tf.truncated_normal([2048, 2048], stddev=0.1))
    b1 = tf.Variable(tf.ones([2048]))

    h1 = tf.nn.relu(tf.matmul(h0, w1) + b1)

    w2 = tf.Variable(tf.truncated_normal([2048, len(rubiks_cube.RubiksCube.OPS)], stddev=0.1))
    b2 = tf.Variable(tf.zeros([len(rubiks_cube.RubiksCube.OPS)]))

    y = tf.nn.softmax(tf.matmul(h1, w2) + b2)
    y_ = tf.placeholder(tf.float32, shape=[None, len(rubiks_cube.RubiksCube.OPS)])

    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    session.run(tf.initialize_all_variables())
    total_loss = 0
    for i in range(200000):
        n = random.randint(1, 40)
        cube, solution = rubiks_cube.RubiksCube().shuffle(n)
        correct = np.zeros(len(rubiks_cube.RubiksCube.OPS))
        correct[rubiks_cube.RubiksCube.OPS.index(solution[0])] = 1
        train_step.run(feed_dict={
            x: [cube.indices()],
            y_: [correct],
        })
        total_loss += cross_entropy.eval(feed_dict={
            x: [cube.indices()],
            y_: [correct],
        })
        if i % 100 == 0:
            print(total_loss / 100)
            total_loss = 0

    mixed_cube, _ = rubiks_cube.RubiksCube().shuffle()
    for i in range(100):
        prediction = session.run(tf.argmax(y, 1), feed_dict={
            x: [mixed_cube.indices()],
        })
        op = rubiks_cube.RubiksCube.OPS[prediction]
        print(mixed_cube)
        print('Predicted op %s' % op)
        input()
        mixed_cube = mixed_cube.do(op)


def embed(embeddings, x):
    return tf.reshape(tf.gather(embeddings, x), [1,540])


if __name__ == '__main__':
    main()
