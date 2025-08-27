# Knowledge-Find

## 1. 개요
문서(PDF, DOCS 등)를 효율적으로 저장하고 검색할 수 있는 웹 서비스입니다. 사용자는 문서를 업로드하고, 필요한 정보를 빠르게 찾을 수 있습니다.
프로젝트는 하이브리드 검색 선택 과제를 함께 수행했습니다.

## 2. 구현된 기능 범위
1. 문서 업로드
드래그 앤 드롭 형식으로 문서를 업로드 할 수 있습니다. 문서는 종류와 개수 상관 없이 여러개의 파일을 업로드 할 수 있습니다. 파일은 지정된 경로에 저장되며, 파일의 메타데이터는 데이터베이스에 저장됩니다.

2. 문서 임베딩
파일이 저장될 때 문서 임베딩이 함께 진행됩니다. 원본 문서의 텍스트를 모델이 처리하기 좋은 형태로 바꾸기 위해 토큰화를 진행합니다. 문장을 의미있는 단위로 쪼개고, 미리 학습된 모델을 통하여 벡터를 생성합니다. 프로젝트에서는 "all-mpnet-base-v2" 모델을 사용했습니다. "all-mpnet-base-v2"는 가벼우면서 한 번에 많은 양의 텍스트를 벡터화 할 수 있는 모델입니다. 백터는 수백 개의 숫자의 리스트이며 의미가 비슷한 문서는 벡터 공간에서 서로 가까운 위치에 배치하게 됩니다. 예를들어 "운동의 효과"와 "체력단련"은 의미가 유사하므로 벡터로 변환하면 매우 가까운 벡터 공간에 위치하게 됩니다.

3. 쿼리
사용자가 검색어를 입력하면 해당 검색어도 동일한 임베딩 모델을 통해 벡터로 변환됩니다. 변환된 벡터를 Qdrant 벡터 데이터베이스에 보낸 후, 가장 유사한 벡터를 찾아냅니다. 이때 문서의 단어를 인덱싱하여 보다 정확한 매칭을 통해 문서를 찾기 위해 키워드 검색을 함꼐 진행합니다. 이는 고유 명사 혹은 특정 단어를 정확하게 찾을 수 있도록 합니다.

4. 결과 반환
Qdrant에서 찾은 결과가 포함된 문서를 웹 페이지에 반환합니다. 검색 결과는 유사도가 높은 순으로 상위에 배치하게 되며, 사용자가 링크를 통해 다운로드 받을 수 있습니다.


## 3. 테스트에 사용한 문사와 종류
PDF, DOCS 등 다양한 문서를 저장 및 검색할 수 있습니다. 테스트 환경에서는 비슷한 카테고리에서 정확한 의미를 추출할 수 있는지 테스트 하기 위해 머신 러닝, 영상 처리, 운동이 미치는 영향에 관한 논문을 사용했습니다.
- Very Deep Convolutional Networks for Large-Scale Image Recognition
- Understanding the difficulty of training deep feedforward neural networks
- Structured Programming with Go To Statements
- Sequence to Sequence Learning with Neural Networks
- Pre-training of Deep Bidirectional Transformers for Language Understanding
- Learning representations by back-propagating errors
- ImageNet Classification with Deep Convolutional Neural Networks
- Health benefits of physical activity- the evidence
- He_Delving_Deep_into_ICCV_2015_paper
- Gradient-based learning applied to document recognition
- GloVe- Global Vectors for Word Representation
- Efficient Estimation of Word Representations in Vector Space
- Effects of Different Kinds of Physical Activity on Vascular Function
- Delving Deep into Rectifiers
- Deep Residual Learning for Image Recognition
- Deep Learning With Depthwise Separable Convolutions
- Batch Normalization
- Attention Is All You Need
- Assran_Self-Supervised_Learning_From_Images_With_a_Joint-Embedding_Predictive_Architecture_CVPR_2023_paper
- A Few-shot Adversarial Learning of Realistic Neural Talking Head Models

## 4. 기술 스택
- Client: Next.js
- Server: FastAPI
- DataBase Storage: PostgreSQL
- Vector DB: Qdrant
- Containerization: Docker

## 5. 실행방법
1. Server, Client 실행
```
# server (python 가상환경 실행 상태)
uvicorn main:app --reload
# client
npm run dev
```

2. 데이터베이스 지정
데이터베이스 설정을 위해 서버에 다음과 같은 파일을 추가합니다. 파일은 "/repository/db_config.py"에 다음과 같이 입력합니다.
```
POSTGRES_DB = {
    "dbname": "설정된 데이터베이스 이름",
    "user": "유저",
    "password": "비밀번호",
    "host": "127.0.0.1",
    "port": "5432",
}
```

3. Docker 실행 (Docker 데스크톱 실행 중일 때)
```
docker run -d \
  --name qdrant-vector-db \
  -p 6333:6333 \
  -v qdrant_data:/qdrant/storage \
  qdrant/qdrant:latest
```

## 6. 결론
프로젝트는 문서 스캔 데이터를 효과적으로 검색하기 위한 하이브리드 검색 시스템을 성공적으로 구축했습니다. 이 시스템은 벡터 검색과 키워드 검색의 장점을 결합하고, RRF(Reciprocal Rank Fusion)을 통해 두 검색 결과의 순위를 융합하여 사용자의 검색 의도를 정확하게 파악하는 데 중점을 두었습니다.

또한 초기 구현 과정에서 이미지, 문서 파싱을 진행하던 중 과도한 GPU 사용으로 인한 문제가 있었지만, 텍스트 벡터화에 집중된 AI 모델을 사용하므로서 문제를 해결했습니다. 적절한 모델을 사용하여 검색 기능 성능 손실 없이 프로그램을 경량화 할 수 있었습니다.

하지만 단어 단위로 벡터화하는 현재 방식에서는 한계를 느낄 수 있었습니다. 검색어의 모호성이 높은 경우 혹은 문장 시퀀스에 대한 연관도를 정확하게 파악하지 못하는 현상이 관찰되었습니다. 예를들어 "effect work out" 검색어의 경우 "운동에 대한 영향"에 대해 결과가 출력되어야 하지만 "effect"단어 자체에 집중되어 검색결과가 일치하지 않는 현상이 있습니다. 이를 해결하기 위해 Qdrnat에 컬렉션 도메인을 세분화 하거나 문장 시퀀스에 대한 벡터를 인식하는 방향으로 발전시킬 수 있을 것으로 생각됩니다.