from urllib.request import urlretrieve
url_prefix = 'https://storage.googleapis.com/gresearch/wit/'
train_template = 'wit_v1.train.all-0000{}-of-00010.tsv.gz' #last wit_v1.train.all-00009-of-00010.tsv.gz
val_template = 'wit_v1.val.all-0000{}-of-00005.tsv.gz' #last wit_v1.val.all-00004-of-00005.tsv.gz
test_template = 'wit_v1.test.all-0000{}-of-00005.tsv.gz' #last wit_v1.test.all-00004-of-00005.tsv.gz
train_files = [train_template.format(str(i)) for i in range(10)]
val_files = [val_template.format(str(i)) for i in range(5)]
test_files = [test_template.format(str(i)) for i in range(5)]

for i,f in enumerate(test_files):
    print(f"Retrieving url {f}")
    urlretrieve(url_prefix+f,f"test-{str(i)}.tsv.gz")

for i,f in enumerate(val_files):
    print(f"Retrieving url {f}")
    urlretrieve(url_prefix+f,f"val-{str(i)}.tsv.gz")

for i,f in enumerate(train_files):
    print(f"Retrieving url {f}")
    urlretrieve(url_prefix+f,f"train-{str(i)}.tsv.gz")
