from .Functions import  preprocess_text, to_sentences, get_Zipf, get_known, count_words, get_word2fameliralty, count_syllables_in_word
from nltk import ngrams, word_tokenize

import numpy as np
class CEScore:
   
    
    def N_grams_comp(self, comp:str, simp:str, n:int):
  
        comp_ngrams = list(ngrams(comp.lower().split(), n))
        simp_ngrams = list(ngrams(simp.lower().split(), n))

      #  if n==1:
       #     return 0
       
        if len(simp_ngrams)==0:
           #print(simp)
           #return self.N_grams_comp(comp,simp,n-1)
           return 0
        counter=0
        for grams_s in simp_ngrams:
          #  found=False
            if grams_s not in comp_ngrams:
            
                for grams_c in comp_ngrams:
                    m_counter=0
                    for s,c in zip(grams_s,grams_c):
                        if s==c:
                            m_counter=m_counter+1
                    if(m_counter>=n-1):
                         counter=counter+((n-2)/n)
                         break
                
            
            else:
                counter=counter+1
        return counter/len(simp_ngrams)
   
    def kept_comp_new(self, ref:str, cand:str):
        
        ref_set = set(ref.split())
        cand_set = set(cand.split())

        I=ref_set.intersection(cand_set)
        U=ref_set.union(cand_set)
        I_score=np.sum([1/(1+get_Zipf(word)) for word in I])
        U_score=np.sum([1/(1+get_Zipf(word)) for word in U])
        return I_score/U_score
       
    
    def Length_Score(self,sentence: str):
        norm_sentence=preprocess_text(sentence)
        words = word_tokenize(norm_sentence)
    
        n=len(words)
      
        
        f=1-(1/(1+np.exp(-0.22*(n-13))))
        return f

    def ASF(self, sentence: str):
    
        words = word_tokenize(sentence)
        words=[word for word in words if word in get_word2fameliralty()]

        if len(words)<1:
            return 0
          
        asf=np.mean([get_known(word)*get_Zipf(word)/(count_syllables_in_word(word)) for word in words])
        return asf
       
    def SSG(self, sentence: str):
    
        norm_sentence=preprocess_text(sentence)
        sentences=[preprocess_text(sent) for sent in to_sentences(sentence) if len(sent) > 1]
        n=count_words(norm_sentence)
    
        if len(sentences)==0:
            sent_sub= 0
        else:
            sent_sub=np.min([ self.ASF(s) *self.Length_Score(s) for s in sentences ])
       
        s= self.ASF(norm_sentence)+5*self.Length_Score(norm_sentence)**0.33
        return 0.45*s+0.55*sent_sub
       

    def GScore(self, comp: str, simp: str):
      
        sentences=[sent for sent in to_sentences(simp)]
    
        gs=0
        sgram=[]
        
     
        for s in sentences:
            ngram=[]
            for n in range(4,8):
                ng=self.N_grams_comp(comp,s,n)
                ngram.append(ng)
            
            if len(ngram)!=0:
                sgram.append(np.mean(ngram))
            
       
        if(len(sgram)==0):
            gs=0
        else:
            gs=np.min(sgram)
          
        return  gs

    def MScore(self, comp: str, simp: str):

        norm_simp=preprocess_text(simp)
        norm_comp=preprocess_text(comp)
        M_score= self.kept_comp_new(norm_comp,norm_simp)
        return M_score

    def SScore(self, comp: str, simp: str):
    
        simp_ssg=self.SSG(simp)
        comp_ssg=self.SSG(comp)
        f= (simp_ssg-comp_ssg)/(comp_ssg+simp_ssg)
        f=f+0.5
        if f<= 1 and f>=0:
            return f
        elif f>1:
            return 1
        else:
            return 0
        
        
    def CEScore(self, comp: str, simp: str):
        
        G=self.GScore(comp,simp)
        S=self.SScore(comp,simp)
        M=self.MScore(comp,simp)
        Gn=1/(1+np.exp(-10*(G-0.5)))
        Sn=1/(1+np.exp(-10*(S-0.5)))
        Mn=1/(1+np.exp(-10*(M-0.5)))
        
        return [S,M,G,(Mn*Sn*Gn)**0.33]
    
    def corpus_CEScore(self, comps:[str], simps: [str]):
        assert  len(comps) == len(simps),"size of arguments are not equals"
        CE=[]
        for comp,simp in zip(comps,simps):
            CE.append(self.CEScore(comp,simp))
        return CE

    