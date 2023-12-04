# Samsara
## Contributor
> Minwoo Kim,		minu928@snu.ac.kr \
  Seungtae Kim,		junglekst@snu.ac.kr		\
  Je-Yeon Jung, 	jyjung22@snu.ac.kr	
## Environment
>  python >= 3.9  
>  numpy  >= 1.20  

### Requirement
	pip install PyYAML

## Plans
* run.py 를 통해서 전체 generative learning을 진행함.  
	- 이때 input file로 ./inputs/input.yaml을 받는다.  
		+ input.yaml 의 구조 : BASE, FF, MD, QM이 크게 있습니다. 
			>   **BASE** : 전체 학습관련된 값들 (슬럼 아이디 등등)  
				**FF**   : train과 관련된 값들  
				**MD**   : md를 돌릴때 필요한 값들  
				**QM**   : 양자 계산을 위한 값들  
* run에서 FF -> MD -> QM 의 과정을 반복함.  
	- 모든 FF, MD, QM의 _program속 세부 파일들을 그 상위 폴더 interface.py를 **상속**받아서 처리하게끔 해야함. (공통된 부분은 묶어야함)  

## ToDo
### in BASE
- **난이도 (Expected)** : [⭐⭐⭐]
- **진행 상황** : `Not Yet`
- **작업 목록**
  	1.  작업 제출 관련된 작업을 해야함

### in FF
- **난이도 (Expected)** : [⭐⭐⭐]
- **진행 상황** : `Not Yet`
- **작업 목록**
	1.  Interface와 Dataclass를 작성해야함.
 	2.  DeePMD-kit과 연결
  	3.  Allegro or Nequip과 연결
  	4.  MACE와 연결...?
     
### FF to MD
- **난이도 (Expected)** : [⭐]
- **진행 상황** : `Pause`
- **작업 목록**
  	1.  Adapter Pattern으로 단순하게 LAMMPS용으로 붙일 예정..
  	  
### in MD
- **난이도 (Expected)** : [⭐⭐]
- **진행 상황** : `Pause`
- **작업 목록**  
	~~1.  Interface와 Dataclass를 작성해야함.~~  
 	~~2.  LAMMPS 관련 스크립트 작성하는 코드를 작성해야함.~~
  	3. 앞 뒤 연결부분 관련 수정 요함 ( 마지막 )
  
### MD to QM
- **난이도 (Expected)** : [⭐⭐⭐⭐]
- **진행 상황** : `Pause`
- **작업 목록**
  	1.  Trajectory를 정리하는 코드
  	2.  평가 기준을 받고 (다양한 평가 기준을 넣을 수 있게), Evaluate한다.
  	3.  Selection of Evaluated Data
  
### QM
- **난이도 (Expected)** : [⭐⭐]
- **진행 상황** : `Not Yet`
- **작업 목록**
	1.  Interface와 Dataclass를 작성해야함.
 	2.  CP2K 관련 스크립트 작성하는 코드를 작성해야함.
     
### QM to FF
- **난이도 (Expected)** : [⭐]
- **진행 상황** : `Pause`
- **작업 목록**
  	1.  데이터를 다시 리-패키징한다.
  	2.  데이터를 다시 스크립트에 넣고 돌린다.
