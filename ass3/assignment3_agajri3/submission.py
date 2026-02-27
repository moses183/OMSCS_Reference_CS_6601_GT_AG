import sys

'''
WRITE YOUR CODE BELOW.
'''
from numpy import zeros, float32
#  pgmpy͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import pgmpy
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
#You are not allowed to use following set of modules from 'pgmpy' Library.͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
#
# pgmpy.sampling.*͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# pgmpy.factors.*͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
# pgmpy.estimators.*͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
import random

def make_security_system_net():
    """
        Create a Bayes Net representation of the above security system problem. 
        Use the following as the name attribute: "H","C", "M","B", "Q", 'K",
        "D"'. (for the tests to work.)
    """
    BayesNet = BayesianNetwork()
    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃    
    #raise NotImplementedError
    BayesNet.add_node("H")
    BayesNet.add_node("M")
    BayesNet.add_node("C")
    BayesNet.add_node("B")
    BayesNet.add_edge("H","Q")
    BayesNet.add_edge("B", "K")
    BayesNet.add_edge("K", "D")
    BayesNet.add_edge("C", "Q")
    BayesNet.add_edge("M", "K")
    BayesNet.add_edge("Q", "D")

    return BayesNet


def set_probability(bayes_net):
    """
        Set probability distribution for each node in the security system.
        Use the following as the name attribute: "H","C", "M","B", "Q", 'K",
        "D"'. (for the tests to work.)
    """
    # TODO: set the probability distribution for each node͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
    cpd_H = TabularCPD('H', 2, values=[[0.5], [0.5]])
    cpd_C = TabularCPD('C', 2, values=[[0.7], [0.3]])
    cpd_M = TabularCPD('M', 2, values=[[0.2], [0.8]])
    cpd_B = TabularCPD('B', 2, values=[[0.5], [0.5]])
    cpd_QCH = TabularCPD('Q', 2, values=[[0.95, 0.45, 0.75, 0.1],
                                         [0.05, 0.55, 0.25, 0.9]], evidence=['C', 'H'], evidence_card=[2, 2])
    cpd_KBM = TabularCPD('K', 2, values=[[0.25, 0.05, 0.99, 0.85],
                                         [0.75, 0.95, 0.01, 0.15]], evidence=['B', 'M'], evidence_card=[2, 2])
    cpd_DQK = TabularCPD('D', 2, values=[[0.98, 0.65, 0.4, 0.01],
                                         [0.02, 0.35, 0.6, 0.99]], evidence=['Q', 'K'], evidence_card=[2, 2])
    bayes_net.add_cpds(cpd_H, cpd_C,cpd_M, cpd_B, cpd_QCH, cpd_KBM, cpd_DQK)


    return bayes_net



def get_marginal_double0(bayes_net):
    """
        Calculate the marginal probability that Double-0 gets compromised.
    """
    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
    solver = VariableElimination(bayes_net)
    marginal_prob = solver.query(variables=['D'], joint=False)
    double0_prob = marginal_prob['D'].values[1]
    return double0_prob


def get_conditional_double0_given_no_contra(bayes_net):
    """
        Calculate the conditional probability that Double-0 gets compromised
        given Contra is shut down.
    """
    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
   # raise NotImplementedError
    solver = VariableElimination(bayes_net)
    conditional_prob = solver.query(variables=['D'], evidence={'C': 0}, joint=False)
    double0_prob = conditional_prob['D'].values[1]
    return double0_prob


def get_conditional_double0_given_no_contra_and_bond_guarding(bayes_net):
    """
        Calculate the conditional probability that Double-0 gets compromised
        given Contra is shut down and Bond is reassigned to protect M.
    """
    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
    solver = VariableElimination(bayes_net)
    conditional_prob = solver.query(variables=['D'], evidence={'B':1,'C': 0}, joint=False)
    double0_prob = conditional_prob['D'].values[1]
    return double0_prob


def get_game_network():
    """
        Create a Bayes Net representation of the game problem.
        Name the nodes as "A","B","C","AvB","BvC" and "CvA".  
    """
    BayesNet = BayesianNetwork()
    BayesNet.add_node("A")
    BayesNet.add_node("C")
    BayesNet.add_node("B")
    BayesNet.add_edge("A","AvB")
    BayesNet.add_edge("B","AvB")
    BayesNet.add_edge("A", "CvA")
    BayesNet.add_edge("C", "CvA")
    BayesNet.add_edge("C","BvC")
    BayesNet.add_edge("B","BvC")

    def tp(l):
        lt=[]
        for ele in l:
            lt.append([ele])
        return lt
    def tp2(l):
        l2=[list(row) for row in zip(*l)]
        return l2

    prior_skill=[0.15,0.45,0.30,0.10]
    priorskill_tp=tp(prior_skill)
    skill_diff1={0:[0.10,0.10,0.80],1:[0.20,0.60,0.20],2:[0.15,0.75,0.10],3:[0.05,0.90,0.05]}
    skill_diff2={0:[0.10,0.10,0.80],1:[0.60,0.20,0.20],2:[0.75,0.15,0.10],3:[0.90,0.05,0.05]}


    def XvYmake(X,Y,XvY):
        skill=[0,1,2,3]
        sdiff=[]
        for x in skill:
            for y in skill:
                diff=abs((x-y))
                if x>y:
                    sdiff.append(skill_diff2[diff])
                elif y>=x:
                    sdiff.append(skill_diff1[diff])
        return TabularCPD(XvY,3,tp2(sdiff),[X,Y],[4,4])


    A_cpd=TabularCPD('A', 4, values=priorskill_tp)
    B_cpd=TabularCPD('B', 4, values=priorskill_tp)
    C_cpd=TabularCPD('C', 4, values=priorskill_tp)
    AvB_cpd=XvYmake("A","B","AvB")
    BvC_cpd=XvYmake("B","C","BvC")
    CvA_cpd=XvYmake("C","A","CvA")

    BayesNet.add_cpds(A_cpd,B_cpd,C_cpd,AvB_cpd,BvC_cpd,CvA_cpd)



    # TODO: fill this out͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError

    return BayesNet


def calculate_posterior(bayes_net):
    """
        Calculate the posterior distribution of the BvC match given that A won against B and tied C. 
        Return a list of probabilities corresponding to win, loss and tie likelihood.
    """
    posterior = [0,0,0]
    infergame=VariableElimination(bayes_net)
    evidence={"AvB":0,"CvA":2}
    BvCpost=infergame.query(variables=["BvC"],evidence=evidence)
    posterior=BvCpost.values

    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃    
    #raise NotImplementedError
    return posterior # list 


def Gibbs_sampler(bayes_net, initial_state):
    """
        Complete a single iteration of the Gibbs sampling algorithm 
        given a Bayesian network and an initial state value. 
        
        initial_state is a list of length 6 where: 
        index 0-2: represent skills of teams A,B,C (values lie in [0,3] inclusive)
        index 3-5: represent results of matches AvB, BvC, CvA (values lie in [0,2] inclusive)
        
        Returns the new state sampled from the probability distribution as a tuple of length 6.
        Return the sample as a tuple. 

        Note: You are allowed to calculate the probabilities for each potential variable
        to be sampled. See README for suggested structure of the sampling process.
    """
    def cal_joint(A,B,C,AvB,BvC,CvA):
        A_cpd=bayes_net.get_cpds("A").values
        B_cpd=bayes_net.get_cpds("B").values
        C_cpd=bayes_net.get_cpds("C").values
        AvB_cpd=bayes_net.get_cpds("AvB").values
        BvC_cpd=bayes_net.get_cpds("BvC").values
        CvA_cpd=bayes_net.get_cpds("CvA").values
        joint=1.0
        joint=A_cpd[A]*B_cpd[B]*C_cpd[C]*AvB_cpd[AvB][A][B]*BvC_cpd[BvC][B][C]*CvA_cpd[CvA][C][A]
        return joint

    if initial_state is None or len(initial_state)==0:
        initial_state=[random.choice([0,1,2,3]),random.choice([0,1,2,3]),random.choice([0,1,2,3]),0,random.choice([0,1,2]),2]
    sample = initial_state.copy()
    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    skill_levels=[0,1,2,3]
    variable_index = random.choice([0,1,2,4]) # Your chosen variable

    #print(f"Variable index: {variable_index}")

    if variable_index == 0:
        # Sample A͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
        A_cpd=bayes_net.get_cpds("A")
        tt=A_cpd.values
        probA=[]
        #print(tt)
        for s in skill_levels:
            newA=cal_joint(s,sample[1],sample[2],sample[3],sample[4],sample[5])
            probA.append(newA)
        probA=[float(i)/sum(probA) for i in probA]
        newA = random.choices([0, 1, 2, 3], probA)

        #print(newA)
        sample[0]=newA[0]
    elif variable_index == 1:
        # Sample B͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
        B_cpd = bayes_net.get_cpds("B")
        tt = B_cpd.values
        probB = []
        # print(tt)
        for s in skill_levels:
            newB=cal_joint(sample[0],s,sample[2],sample[3],sample[4],sample[5])
            probB.append(newB)
        probB=[float(i)/sum(probB) for i in probB]

        newB = random.choices([0, 1, 2, 3], probB)

        #print(newB)
        sample[1] = newB[0]
    elif variable_index == 2:
        # Sample C͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
        C_cpd = bayes_net.get_cpds("C")
        tt = C_cpd.values
        probC = []
        # print(tt)
        for s in skill_levels:
            newC=cal_joint(sample[0],sample[1],s,sample[3],sample[4],sample[5])
            probC.append(newC)
        probC=[float(i)/sum(probC) for i in probC]

        newC = random.choices([0, 1, 2, 3], probC)

        #print(newC)
        sample[2] = newC[0]

    elif variable_index == 4:
        # Sample BvC͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
        BvC_cpd = bayes_net.get_cpds("BvC")
        C=sample[2]
        B=sample[1]
        mt = BvC_cpd.values
        tb = [mt[0][B][C], mt[1][B][C], mt[2][B][C]]
        probBvC=[]
        for j in [0,1,2]:
            newBvC=cal_joint(sample[0],sample[1],sample[2],sample[3],j,sample[5])
            probBvC.append(newBvC)
        probBvC=[i/sum(probBvC) for i in probBvC]
        #print(probBvC)
        #print(mt)

        newBvC = random.choices([0, 1, 2], probBvC)

        #print(newBvC)
        sample[4] = newBvC[0]
    
    else:
        raise ValueError("Variable index out of range")

    sample=tuple(sample)
    #print(sample)

    return sample


def MH_sampler(bayes_net, initial_state):
    """
        Complete a single iteration of the MH sampling algorithm given a Bayesian network and an initial state value. 
        initial_state is a list of length 6 where: 
        index 0-2: represent skills of teams A,B,C (values lie in [0,3] inclusive)
        index 3-5: represent results of matches AvB, BvC, CvA (values lie in [0,2] inclusive)    
        Returns the new state sampled from the probability distribution as a tuple of length 6. 
    """
    """
    A_cpd = bayes_net.get_cpds("A")      
    AvB_cpd = bayes_net.get_cpds("AvB")
    match_table = AvB_cpd.values
    team_table = A_cpd.values
    """
    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃

    def cal_joint(A,B,C,AvB,BvC,CvA):
        A_cpd=bayes_net.get_cpds("A").values
        B_cpd=bayes_net.get_cpds("B").values
        C_cpd=bayes_net.get_cpds("C").values
        AvB_cpd=bayes_net.get_cpds("AvB").values
        BvC_cpd=bayes_net.get_cpds("BvC").values
        CvA_cpd=bayes_net.get_cpds("CvA").values
        joint=1.0
        joint=A_cpd[A]*B_cpd[B]*C_cpd[C]*AvB_cpd[AvB][A][B]*BvC_cpd[BvC][B][C]*CvA_cpd[CvA][C][A]
        return joint

    if initial_state is None or len(initial_state)==0:
        initial_state=[random.choice([0,1,2,3]),random.choice([0,1,2,3]),random.choice([0,1,2,3]),0,random.choice([0,1,2]),2]

    newst=[random.choice([0,1,2,3]),random.choice([0,1,2,3]),random.choice([0,1,2,3]),0,random.choice([0,1,2]),2]

    likeinit=1.0
    likenew=1.0

    likeinit=cal_joint(initial_state[0],initial_state[1],initial_state[2],initial_state[3],initial_state[4],initial_state[5])
    likenew=cal_joint(newst[0],newst[1],newst[2],newst[3],newst[4],newst[5])
    '''
    vars=["A","B","C","AvB","BvC","CvA"]
    AvB_cpd=bayes_net.get_cpds("AvB").values
    BvC_cpd=bayes_net.get_cpds("BvC").values
    CvA_cpd=bayes_net.get_cpds("CvA").values
    skill_levels=[0,1,2,3]
    for i in [0,1,2,4]:
        if i<3:

            tt= bayes_net.get_cpds(vars[i]).values
            likeinit*=tt[initial_state[i]]
            likenew*=tt[newst[i]]
        if i==4:
            Bi=initial_state[1]
            Ci=initial_state[2]
            Bn=newst[1]
            Cn=newst[2]
            #mt = infergame.query(variables=[vars[i]], evidence=evidence).values
            mt= bayes_net.get_cpds(vars[i]).values
            tbi= [mt[0][Bi][Ci],mt[1][Bi][Ci],mt[2][Bi][Ci]]
            #print(Bi,Ci,Bn,Cn,mt,tbi,sep="\n")
            tbn= [mt[0][Bn][Cn],mt[1][Bn][Cn],mt[2][Bn][Cn]]
            likeinit*=tbi[initial_state[i]]
            likenew*=tbn[newst[i]]
    Ai=initial_state[0]
    Ci=initial_state[2]
    Bi=initial_state[1]
    An=newst[0]
    Bn=newst[1]
    Cn=newst[2]
    likeinit=likeinit*AvB_cpd[0][Ai][Bi]*CvA_cpd[2][Ci][Ai]
    likenew=likenew*AvB_cpd[0][An][Bn]*CvA_cpd[2][Cn][An]
    '''
    likerat=likenew/likeinit
    likerat=min(likerat,1)
    u=random.uniform(0,1)
    if u < likerat:
        return tuple(newst)
    else:
        return tuple(initial_state)



def compare_sampling(bayes_net, initial_state):
    """
        Compare Gibbs and Metropolis-Hastings sampling by calculating how long it takes for each method to converge.
    """
    def norma(l):
        nl=l.copy()
        if sum(l)==0:
            return [0.0,0.0,0.0]
        for i in range(len(l)):
            nl[i]=float(l[i]/sum(l))
        return nl

    burnin = 50
    Gibbs_count = -burnin
    MH_count = -burnin
    MH_rejection_count = 0
    Gibbs_convergence = [0,0,0] # posterior distribution of the BvC match as produced by Gibbs 
    MH_convergence = [0,0,0] # posterior distribution of the BvC match as produced by MH
    N=100
    delta=0.001
    past=[0,0,0]
    n=0
    pst=initial_state.copy()
    prob_diff=0
    while True :
        newst=Gibbs_sampler(bayes_net, pst)
        pst=list(newst).copy()
        Gibbs_count = Gibbs_count + 1
        bvcst=newst[4]
        past=Gibbs_convergence.copy()
        #print(f"past {past}")
        pastprob=norma(past)
        #print(pastprob)
        Gibbs_convergence[bvcst]+=1
        #print(f"new {Gibbs_convergence}")
        prob=norma(Gibbs_convergence)
        #print(prob)
        #prob_diff=abs(prob[0]-pastprob[0])+abs(prob[1]-pastprob[1])+abs(prob[2]-pastprob[2])
        prev_prob_diff=prob_diff
        prob_diff=0
        for j in range(len(pastprob)):
            prob_diff+=abs(pastprob[j]-prob[j])
            #prob_diff = max(prob_diff, abs(pastprob[j] - prob[j]))
        #print(prob_diff)
        if prob_diff<delta:
            n+=1
        if n==N and Gibbs_count>0:
            break
    Gibbs_convergence=prob.copy()

    past = [0, 0, 0]
    pastprob = norma(past)
    pst = initial_state.copy()
    probdiff=0
    n=0
    while True:
        newst=MH_sampler(bayes_net, pst)
        MH_count = MH_count + 1
        if pst == list(newst):
            MH_rejection_count = MH_rejection_count + 1
        pst = list(newst).copy()
        bvcst=newst[4]
        past= MH_convergence.copy()
        pastprob=norma(past)
        MH_convergence[bvcst]+=1
        prob= norma(MH_convergence)
        #prob_diff=abs(prob[0]-pastprob[0])+abs(prob[1]-pastprob[1])+abs(prob[2]-pastprob[2])
        prev_prob_diff=prob_diff
        prob_diff=0
        for j in range(len(pastprob)):
            prob_diff+=abs(pastprob[j]-prob[j])
            #prob_diff=max(prob_diff,abs(pastprob[j]-prob[j]))
        #print(prob_diff)
        if prob_diff < delta:
            n += 1

        if n == N and MH_count>0:
            break
    MH_convergence=prob.copy()



    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
    return Gibbs_convergence, MH_convergence, Gibbs_count, MH_count, MH_rejection_count


def sampling_question():
    """
        Question about sampling performance.
    """
    # TODO: assign value to choice and factor͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError
    Gibbs_convergence, MH_convergence, Gibbs_count, MH_count, MH_rejection_count=compare_sampling(get_game_network(),[])
    choice = 2
    options = ['Gibbs','Metropolis-Hastings']
    factor = 0
    print(f"{Gibbs_convergence}, {MH_convergence}, {Gibbs_count}, {MH_count}, {MH_rejection_count}")
    if Gibbs_count >= MH_count:
        choice=1
        factor=Gibbs_count/MH_count
    elif Gibbs_count < MH_count:
        choice=0
        factor=MH_count/Gibbs_count
    return options[choice], factor


def return_your_name():
    """
        Return your name from this function
    """
    return "Aarushi Gajri"
    # TODO: finish this function͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄐͏󠄃͏︃
    #raise NotImplementedError


if __name__ == "__main__":
    #print(Gibbs_sampler(get_game_network(),[0, 2, 3, 0, 2, 2]))
    print(sampling_question())
