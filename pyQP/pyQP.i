// pyQP.i - SWIG interface

%module pyQP
%{
#include "Array.h"
#include "QuadProg++.h"
%}
/* Parse the header file to generate wrappers */

//%include "Array.h"
//%include "QuadProg++.h"

//%template(Matrixd)  QuadProgPP::Matrix<double>;
//%template(Vectord)  QuadProgPP::Vector<double>;

%{
#define SWIG_FILE_WITH_INIT
%}
%include "numpy.i"
%init %{
    import_array();
%}


%apply (double* INPLACE_ARRAY1, int DIM1) {(double* g0,   int n_g0),
                                           (double* ce0, int n_ce0),
                                           (double* ci0, int n_ci0)};
%apply (double* INPLACE_ARRAY2, int DIM1, int DIM2) {(double* G,  int Grow,  int Gcol),
                                                     (double* CE, int CErow, int CEcol),
                                                     (double* CI, int CIrow, int CIcol)};
%apply (double* ARGOUT_ARRAY1, int DIM1 ) {(double* X, int n_X)};


//Management of exceptions raised by QuadProg++
%include exception.i
%exception { 
    try {
        $action
    } catch(std::logic_error &e) {
        std::cout<<e.what()<<std::endl;
        SWIG_exception(SWIG_RuntimeError, "std::logic_error exception raised form QuadProg++");
    } catch(std::runtime_error &e) {
        std::cout<<e.what()<<std::endl;
        SWIG_exception(SWIG_RuntimeError, "std::runtime_error exception  raised form QuadProg++");
    } catch (...) {
        SWIG_exception(SWIG_RuntimeError, "unknown exception!");
    }
}


%inline
%{
  void _solve_quadprog(double* G,  int Grow,  int Gcol,
              double* g0,   int n_g0,
              double* CE, int CErow, int CEcol,
              double* ce0, int n_ce0,
              double* CI, int CIrow, int CIcol,
              double* ci0, int n_ci0,
              double* X, int n_X)
    {
        QuadProgPP::Matrix<double> _G(G, Grow, Gcol);
        QuadProgPP::Matrix<double> _CE(CE, CErow, CEcol);
        QuadProgPP::Matrix<double> _CI(CI, CIrow, CIcol);
        
        QuadProgPP::Vector<double> _g0(g0, n_g0);
        QuadProgPP::Vector<double> _ce0(ce0, n_ce0);
        QuadProgPP::Vector<double> _ci0(ci0, n_ci0);
        QuadProgPP::Vector<double> _X(n_X);
        
        QuadProgPP::solve_quadprog(_G, _g0, _CE, _ce0, _CI, _ci0, _X);
        
        for (int i=0; i<n_X; i++)
            X[i] = _X[i];
    }
%}




%pythoncode {

    def solve_qp(G, g0, CE_T, ce0, CI_T, ci0):
        """ Solve quadratic problem in the QuadProg++ formulation.
        
        It solves the following problem:
        
            min(x) (.5 x.T G x + g0.T x + r)
            
            s.t.:   CE x + ce0 =  0
                    CI x + ci0 >= 0
        """
        import numpy as np
        _G    = np.ascontiguousarray(G,  dtype=np.float64)
        _g0   = np.ascontiguousarray(g0, dtype=np.float64)
        _CE_T = np.ascontiguousarray(CE_T, dtype=np.float64)
        _ce0  = np.ascontiguousarray(ce0,  dtype=np.float64)
        _CI_T = np.ascontiguousarray(CI_T, dtype=np.float64)
        _ci0  = np.ascontiguousarray(ci0,  dtype=np.float64)
        return _solve_quadprog(_G, _g0, _CE_T, _ce0, _CI_T, _ci0, _g0.shape[0])



    def solve_qp_as_cvxopt(P, q, G, h, A, b):
        """ Solve quadratic problem in the CvxOpt formulation.
        
        It solves the following problem (as defined in the cvxopt package):
        
            min(x) (.5 x.T P x + q.T x + r)
            
            s.t.:   A x =  b
                    G x <= h
        """
        import numpy as np
        P    = np.ascontiguousarray(P, dtype=np.float64)
        q    = np.ascontiguousarray(q, dtype=np.float64)
        CE_T = np.ascontiguousarray(np.asanyarray(A).T,  dtype=np.float64)
        ce0  = np.ascontiguousarray(-np.asanyarray(b),   dtype=np.float64)
        CI_T = np.ascontiguousarray(-np.asanyarray(G).T, dtype=np.float64)
        ci0  = np.ascontiguousarray(h, dtype=np.float64)
        x =  _solve_quadprog(P, q, CE_T, ce0, CI_T, ci0, q.shape[0])
        return x

}




