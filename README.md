# Intuitive Physics Challenge 2019

This repo contains code that produces submission.zip file under the guideline at [https://intphys.com/challenge.html](https://intphys.com/challenge.html)

## Steps

* Download **test.O1.tar.gz**, **test.O2.tar.gz** and **test.O3.tar.gz** from [https://intphys.com/download.html#download](https://intphys.com/download.html#download)

* Put **.py** files in this repo in the uncompressed folder **test**

* Run following command to generate **answer.txt**

```
python check_shape_consistent.py -f task.txt
```

* Zip **answer.txt** into **submission.zip** and check validity before submission

```
./validate submission.zip task.txt 
