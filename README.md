# FindPlayground


#### Vertis Testing Server ####
URL: http://fpg.pydevs.vertis  
  
#### Staging Server  
No staging server is setup.

#### System Requirements  
+ python2.7  
+ django1.8  
+ postgresql9.1  

#### Installation
    _ Needs to add this section _ 
  
#### Deploying continous builds on pydevs.com  
+ update the required branch on stash.
+ run below command:  

		fab rebuild:{branchname} -H pydevs.com -u username  
		
