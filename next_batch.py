import numpy as np
import pandas as pd
 
class DataSet(object):
 
    def __init__(self, images, labels, num_examples):
        self._images = images
        self._labels = labels
        self._epochs_completed = 0  # 完成遍历轮数
        self._index_in_epochs = 0   # 调用next_batch()函数后记住上一次位置
        self._num_examples = num_examples  # 训练样本数
 
    def next_batch(self, batch_size, fake_data=False, shuffle=True):
        start = self._index_in_epochs

        # 将训练样本数据进行shuffle
        if self._epochs_completed == 0 and start == 0 and shuffle:
            index0 = np.arange(self._num_examples)
            np.random.shuffle(index0)
            self._images = np.array(self._images)[index0]
            self._labels = np.array(self._labels)[index0]

        #如果已经走完一遍了，那么重头继续走
        if start + batch_size > self._num_examples:
            self._epochs_completed += 1
            rest_num_examples = self._num_examples - start
            images_rest_part = self._images[start:self._num_examples]
            labels_rest_part = self._labels[start:self._num_examples]
            if shuffle:
                index = np.arange(self._num_examples)
                np.random.shuffle(index)
                self._images = self._images[index]
                self._labels = self._labels[index]
            start = 0
            self._index_in_epochs = batch_size - rest_num_examples
            end = self._index_in_epochs
            images_new_part = self._images[start:end]
            labels_new_part = self._labels[start:end]
            return np.concatenate((images_rest_part, images_new_part), axis=0), np.concatenate(
                (labels_rest_part, labels_new_part), axis=0)
 
        else:
            self._index_in_epochs += batch_size
            end = self._index_in_epochs
            return self._images[start:end], self._labels[start:end]
 
 
if __name__ == '__main__':
    data = pd.read_csv("feature.csv")
    y = np.array(data['Survived'])
    X = data.drop(['Survived'], axis=1)
    X = np.array(X)
    #input = ['a', 'b', '1', '2', '*', '3', 'c', '&', '#']
    #output = ["Letter", "Letter", "Number", "Number", "Symbol", "Number", "Letter", "Symbol", "Symbol"]
    ds = DataSet(X, y, 891)
    for i in range(3):
        image_batch, label_batch = ds.next_batch(4)
        print(image_batch)
        print(label_batch)