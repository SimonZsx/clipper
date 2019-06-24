### FatigueDetection

Structure see DAG description.png.

Input: Image, need to serialize to json string

Output: A boolean value indicating whether the driver is sleepling or not.

GPU:

open-cv: container 1-4

tensorflow: container 3

<br/>

## Container Information
This application consists for six containers.

#### Container1: string transformer. 
Input: audio file `(.jpg)`; Output: `String`

#### Container2: face extractor
Input: image file  `string`; Output: `String` 

#### Container3: drowiness detector
Input: String; Output: String

#### Container4: human segmentation
Input: `String`; Output: `String`

### Container5: pose analyzer
Input: `String`; Output: `String`

### Container6: conclusion
Input: `String`; Output: `String`

### Dataset:

https://susanqq.github.io/UTKFace/

UTKFace dataset is a large-scale face dataset with long age span (range from 0 to 116 years old). The dataset consists of over 20,000 face images with annotations of age, gender, and ethnicity. The images cover large variation in pose, facial expression, illumination, occlusion, resolution, etc. 


