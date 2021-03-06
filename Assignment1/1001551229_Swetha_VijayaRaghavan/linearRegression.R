# Setting up the environment and importing the Iris data
setwd('/Users/swethavijayaraghavan/Desktop/1001551229_Swetha_VijayaRaghavan')
library('MASS')
data<-read.csv('iris.txt',header=FALSE) 
irisData<-data
irisData$V5<-NULL #Removed the classlabel
# Assinging the data in to respectivce A, Y matrices
A<-data.matrix(irisData, rownames.force = NA) # If fails, it return NA
#Transpose of A
transposeA<-t(A)
Y<-matrix(data$V5) #The class lable matrix
# Categorizing the class labels into 3 Integer values
Y<-sapply(data$V5,switch,'Iris-setosa'=0,'Iris-versicolor'=1,'Iris-virginica'=2)

#Applying K-Fold Cross Validation to find error rate
KFoldCrossValidation <- function(A,Y,K){
    randomindex<-sample(length(Y))
    error <- 0
    size<-length(Y)/K
    class<- unique(Y)
    for(i in 1:K){
      testing <- randomindex[ (size*(i-1)+1): (size*i) ]; # Divided the data into Testing Data
      training <- setdiff( 1:length(Y),  testing); # Rest as Training Set
      beta <- linearRegression(A[training, ], Y[training])
      Ypred <- classification(A[testing, ], beta, length(class))
      error <- error + sumOfSquaredError(Ypred, Y[testing])
  }
    error <- error/K
    return(error)
}

# Applying Classification 
classification <- function(testing, beta, classLength){
    Yout <- round(testing%*%beta)
    Yout[ Yout > classLength ] <- classLength
    Yout[Yout < 1] <- 1
    return(Yout)
}

# Sum of squared error using the formula
sumOfSquaredError = function(Yact,Ypred){
  error = Ypred - Yact;
  error = sum(error * error)/length(Ypred);
  return(error)
}

# Applying Linear Regression using the formula
linearRegression <- function(A, Y){
    transposeA<-t(A)
    beta<-ginv(transposeA%*%A)%*%transposeA%*%Y  
    return(beta)
  }

#using the above computed values, by calling the function, it will compute the Average KFold Error
beta<-linearRegression(A,Y)
print(paste("Beta Values:", beta))
K<-3;
KFoldError<-KFoldCrossValidation(A, Y, K)
N <- 10000;
error <- 0;
for (var in 1:N){
  error = error + KFoldCrossValidation(A, Y, K);
}
average = error / N;
print(paste("Avg KFoldCrossValidation_Error : ", KFoldError))
print(paste(average))

