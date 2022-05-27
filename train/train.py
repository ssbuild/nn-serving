import tensorflow as tf
import numpy as np

batch_size = 4
seq_len = 10

x1 = tf.placeholder(tf.float32,shape=(None,seq_len),name="x1")
x2 = tf.placeholder(tf.float32,shape=(None,seq_len),name="x2")
y = tf.placeholder(tf.float32,shape=(None,seq_len),name="label_ids")

output = tf.concat([x1,x2],axis=1)

pred_ids = tf.layers.dense(inputs=output,units=seq_len)

pred_ids = tf.identity(pred_ids,name="pred_ids")
loss = tf.losses.mean_squared_error(y, pred_ids)
train_op = tf.train.GradientDescentOptimizer(0.2).minimize(loss)

init = tf.global_variables_initializer()


with tf.Session() as sess:
    sess.run(init)
    for step in range(10000):
        x1_data = np.random.rand(batch_size,seq_len)
        x2_data = np.random.rand(batch_size, seq_len)
        y_data = x1_data + 2 * x2_data
        _,out = sess.run((train_op,pred_ids),feed_dict={x1:x1_data,x2:x2_data ,y:y_data})
        if step%20==0:
            print(step)
            #print(out)
    save_path = tf.train.Saver().save(sess,"./model.ckpt")
