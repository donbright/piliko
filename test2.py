        from piliko import *
        
        print 'testing projective functions'
        a1=projective_point(1,0)
        a2=projective_point(2,3)
        a3=projective_point(4,-1)
        a4=projective_point(3,5)
        
        f=projective_form(1,0,1)
        q12=projective_quadrance(a1,a2,f)
        q23=projective_quadrance(a2,a3,f)
        q34=projective_quadrance(a3,a4,f)
        q14=projective_quadrance(a1,a4,f)
        
        print 'projective points',a1,a2,a3,a4
        print 'form: ', f
        print 'projective quadrances:',q12,q23,q34,q14
        
        
        
        
        
        
        print 'testing projective functions'
        a1=projective_point(0,1)
        a2=projective_point(0,4)
        a3=projective_point(0,3)
        a4=projective_point(0,7)
        
        q12=quadrance(a1,a2)
        q23=quadrance(a2,a3)
        q34=quadrance(a3,a4)
        q14=quadrance(a1,a4)
        
        print 'projective points',a1,a2,a3,a4
        print 'form: ', f
        print 'projective quadrances:',q12,q23,q34,q14
        print is_harmonic_range(a1,a2,a3,a4)
        print is_harmonic_range(point(q23,0),point(q34,0),point(q12,0),point(q14,0))
        
        
