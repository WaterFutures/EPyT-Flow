"""
This module contains a wrapper for EPyT that allows a better error/warning handling.
"""
from ctypes import byref, create_string_buffer
from epyt import epanet
from epyt.epanet import epanetapi, epanetmsxapi


class EPyT(epanet):
    """
    Wrapper for the `epyt.epanet <https://epanet-python-toolkit-epyt.readthedocs.io/en/latest/api.html#epyt.epanet.epanet>`_ class.
    This wrapper adds functionalities for getting error/warning messages after each
    EPANET function call.
    """
    def __init__(self, *argv, version=2.2, ph=False, loadfile=False, customlib=None,
                 display_msg=True, display_warnings=True):
        super().__init__(*argv, version=version, ph=ph, loadfile=loadfile, customlib=customlib,
                         display_msg=display_msg, display_warnings=display_warnings)

        # Inject custom EPANET API wrapper
        if self.api._ph is not None:
            self.api.ENdeleteproject()
        else:
            self.api.ENclose()

        self.api = MyEpanetAPI(version=version, ph=ph, customlib=customlib)

        self.api.ENopen(self.TempInpFile, self.RptTempfile, self.BinTempfile)

        self.LibEPANETpath = self.api.LibEPANETpath
        self.LibEPANET = self.api.LibEPANET

    def loadMSXFile(self, msxname, customMSXlib=None, ignore_properties=False):
        super().loadMSXFile(msxname, customMSXlib, ignore_properties)

        # Inject custom EPANET-MSX API wrapper
        self.msx.MSXclose()
        self.msx = MyEpanetMsxAPI(msxfile=self.MSXTempFile, customMSXlib=customMSXlib,
                                  display_msg=self.display_msg,
                                  msxrealfile=self.MSXFile)
        return self.msx

    def set_error_handling(self, raise_exception_on_error: bool) -> None:
        """
        Specifies the behavior in the case of an error/warning --
        i.e. should an exception be raised or not?

        Parameters
        ----------
        raise_exception_on_error : `bool`
            True if an exception should be raise, False otherwise.
        """
        self.api.set_error_handling(raise_exception_on_error)

    def was_last_func_successful(self) -> bool:
        """
        Checks if the last EPANET function call was successful.

        Returns
        -------
        `bool`
            True if there was no error/warning, False otherwise.
        """
        return self.api.was_last_func_successful()

    def get_last_error_desc(self) -> str:
        """
        Returns a description of the last error/warning if any occured.
        Returns None if there was no error/warning.

        Returns
        -------
        `str`
            Error/warning description.
        """
        return self.api.get_last_error_desc()

    def get_last_error_code(self) -> int:
        """
        Returns the code of the last error/warning if any occured.
        Returns 0 if there was no error/warning.

        Refer to the `EPANET documentation <http://wateranalytics.org/EPANET/group___warning_codes.html>`_
        for a list of all possible warning codes and their meanings.

        Returns
        -------
        `int`
            Error/warning code.
        """
        return self.api.get_last_error_code()


class MyEpanetMsxAPI(epanetmsxapi):
    """
    Wrapper for the `epyt.epanet.epanetmsxapi <https://epanet-python-toolkit-epyt.readthedocs.io/en/latest/api.html#epyt.epanet.epanetmsxapi>`_
    class adding error/warning storage functionalities.
    """
    def __init__(self, raise_on_error: bool = True, **kwds):
        self.__raise_on_error = raise_on_error
        self.__last_error_code = None
        self.__last_error_desc = None

        super().__init__(**kwds)

    def set_error_handling(self, raise_on_error: bool) -> None:
        """
        Specifies the behavior in the case of an error/warning --
        i.e. should an exception be raised or not?

        Parameters
        ----------
        raise_exception_on_error : `bool`
            True if an exception should be raise, False otherwise.
        """
        self.__raise_on_error = raise_on_error

    def get_last_error_desc(self) -> str:
        """
        Returns the description of the last EPANET-MSX error/warning (if any).

        Returns
        -------
        `str`
            Description of the last error/warning. None, if there was no error/warning.
        """
        return self.__last_error_desc

    def get_last_error_code(self) -> int:
        """
        Returns the code of the last EPANET-MSX error/warnning (if any).

        Refer to the EPANET-MSX user manual for a list of all possible warning codes
        and their meanings.

        Returns
        -------
        `int`
            Code of the last error/warning. 0, if there was no error/warning.
        """
        return self.__last_error_code

    def was_last_func_successful(self) -> bool:
        """
        Checks if the last EPANET-MSX call was successful or not.

        Parameters
        ----------
        `bool`
            True if the last EPANET-MSX call returned an error/warning, False otherwise.
        """
        return self.__last_error_desc is None

    def _reset_error(self) -> None:
        self.__last_error_code = 0
        self.__last_error_desc = None

    def MSXerror(self, err_code: int) -> None:
        error_desc = create_string_buffer(256)
        self.msx_error(err_code, error_desc, 256)
        self.__last_error_code = err_code
        self.__last_error_desc = error_desc.value.decode()

        if self.__raise_on_error:
            raise RuntimeError(self.__last_error_desc)

    def MSXopen(self, msxfile, msxrealfile):
        self._reset_error()
        super().MSXopen(msxfile, msxrealfile)

    def MSXclose(self):
        self._reset_error()
        return super().MSXclose()

    def MSXgetindex(self, obj_type, obj_id):
        self._reset_error()
        return super().MSXgetindex(obj_type, obj_id)

    def MSXgetID(self, obj_type, index, id_len=80):
        self._reset_error()
        return super().MSXgetID(obj_type, index, id_len)

    def MSXgetIDlen(self, obj_type, index):
        self._reset_error()
        return super().MSXgetIDlen(obj_type, index)

    def MSXgetspecies(self, index):
        self._reset_error()
        return super().MSXgetspecies(index)

    def MSXgetcount(self, code):
        self._reset_error()
        return super().MSXgetcount(code)

    def MSXgetconstant(self, index):
        self._reset_error()
        return super().MSXgetconstant(index)

    def MSXgetparameter(self, obj_type, index, param):
        self._reset_error()
        return super().MSXgetparameter(obj_type, index, param)

    def MSXgetpatternlen(self, pattern_index):
        self._reset_error()
        return super().MSXgetpatternlen(pattern_index)

    def MSXgetpatternvalue(self, pattern_index, period):
        self._reset_error()
        return super().MSXgetpatternvalue(pattern_index, period)

    def MSXgetinitqual(self, obj_type, index, species):
        self._reset_error()
        return super().MSXgetinitqual(obj_type, index, species)

    def MSXgetsource(self, node_index, species_index):
        self._reset_error()
        return super().MSXgetsource(node_index, species_index)

    def MSXsaveoutfile(self, filename):
        self._reset_error()
        super().MSXsaveoutfile(filename)

    def MSXsavemsxfile(self, filename):
        self._reset_error()
        super().MSXsavemsxfile(filename)

    def MSXsetconstant(self, index, value):
        self._reset_error()
        super().MSXsetconstant(index, value)

    def MSXsetparameter(self, obj_type, index, param, value):
        self._reset_error()
        super().MSXsetparameter(obj_type, index, param, value)

    def MSXsetinitqual(self, obj_type, index, species, value):
        self._reset_error()
        super().MSXsetinitqual(obj_type, index, species, value)

    def MSXsetpattern(self, index, factors, nfactors):
        self._reset_error()
        super().MSXsetpattern(index, factors, nfactors)

    def MSXsetpatternvalue(self, pattern, period, value):
        self._reset_error()
        super().MSXsetpatternvalue(pattern, period, value)

    def MSXsolveQ(self):
        self._reset_error()
        super().MSXsolveQ()

    def MSXsolveH(self):
        self._reset_error()
        super().MSXsolveH()

    def MSXaddpattern(self, pattern_id):
        self._reset_error()
        super().MSXaddpattern(pattern_id)

    def MSXusehydfile(self, filename):
        self._reset_error()
        super().MSXusehydfile(filename)

    def MSXstep(self):
        self._reset_error()
        return super().MSXstep()

    def MSXinit(self, flag):
        self._reset_error()
        super().MSXinit(flag)

    def MSXreport(self):
        self._reset_error()
        super().MSXreport()

    def MSXgetqual(self, type, index, species):
        self._reset_error()
        return super().MSXgetqual(type, index, species)

    def MSXsetsource(self, node, species, type, level, pat):
        self._reset_error()
        super().MSXsetsource(node, species, type, level, pat)


class MyEpanetAPI(epanetapi):
    """
    Wrapper for the `epyt.epanet.epanetapi <https://epanet-python-toolkit-epyt.readthedocs.io/en/latest/api.html#epyt.epanet.epanetapi>`_
    class adding error/warning storage functionalities.
    """
    def __init__(self, raise_on_error: bool = True, **kwds):
        self.__raise_on_error = raise_on_error
        self.__last_error_code = None
        self.__last_error_desc = None

        super().__init__(**kwds)

    def set_error_handling(self, raise_on_error: bool) -> None:
        """
        Specifies the behavior in the case of an error/warning --
        i.e. should an exception be raised or not?

        Parameters
        ----------
        raise_exception_on_error : `bool`
            True if an exception should be raise, False otherwise.
        """
        self.__raise_on_error = raise_on_error

    def get_last_error_desc(self) -> str:
        """
        Returns the description of the last EPANET error/warning (if any).

        Returns
        -------
        `str`
            Description of the last error/warning. None, if there was no error/warning.
        """
        return self.__last_error_desc

    def get_last_error_code(self) -> int:
        """
        Returns the code of the last EPANET error/warnning (if any).

        Refer to the `EPANET documentation <http://wateranalytics.org/EPANET/group___warning_codes.html>`_
        for a list of all possible warning codes and their meanings.

        Returns
        -------
        `int`
            Code of the last error/warning. 0, if there was no error/warning.
        """
        return self.__last_error_code

    def was_last_func_successful(self) -> bool:
        """
        Checks if the last EPANET call was successful or not.

        Parameters
        ----------
        `bool`
            True if the last EPANET call returned an error/warning, False otherwise.
        """
        return self.__last_error_desc is None

    def _reset_error(self) -> None:
        self.__last_error_code = 0
        self.__last_error_desc = None

    def _check_for_error(self) -> None:
        if self.errcode != 0:
            error_desc = create_string_buffer(150)
            self._lib.ENgeterror(self.errcode, byref(error_desc), 150)

            self.__last_error_code = self.errcode
            self.__last_error_desc = error_desc.value.decode()

            if self.__raise_on_error:
                raise RuntimeError(self.__last_error_desc)

    def ENepanet(self, inpfile="", rptfile="", binfile=""):
        self._reset_error()
        super().ENepanet(inpfile, rptfile, binfile)
        self._check_for_error()

    def ENaddcontrol(self, conttype, lindex, setting, nindex, level):
        self._reset_error()
        r = super().ENaddcontrol(conttype, lindex, setting, nindex, level)
        self._check_for_error()
        return r

    def ENaddcurve(self, cid):
        self._reset_error()
        super().ENaddcurve(cid)
        self._check_for_error()

    def ENadddemand(self, nodeIndex, baseDemand, demandPattern, demandName):
        self._reset_error()
        super().ENadddemand(nodeIndex, baseDemand, demandPattern, demandName)
        self._check_for_error()

    def ENaddlink(self, linkid, linktype, fromnode, tonode):
        self._reset_error()
        r = super().ENaddlink(linkid, linktype, fromnode, tonode)
        self._check_for_error()
        return r

    def ENaddnode(self, nodeid, nodetype):
        self._reset_error()
        r = super().ENaddnode(nodeid, nodetype)
        self._check_for_error()
        return r

    def ENaddpattern(self, patid):
        self._reset_error()
        super().ENaddpattern(patid)
        self._check_for_error()

    def ENaddrule(self, rule):
        self._reset_error()
        super().ENaddrule(rule)
        self._check_for_error()

    def ENclearreport(self):
        self._reset_error()
        super().ENclearreport()
        self._check_for_error()

    def ENclose(self):
        self._reset_error()
        super().ENclose()
        self._check_for_error()

    def ENcloseH(self):
        self._reset_error()
        super().ENcloseH()
        self._check_for_error()

    def ENcloseQ(self):
        self._reset_error()
        super().ENcloseQ()
        self._check_for_error()

    def ENcopyreport(self, filename):
        self._reset_error()
        super().ENcopyreport(filename)
        self._check_for_error()

    def ENcreateproject(self):#
        self._reset_error()
        super().ENcreateproject()
        self._check_for_error()

    def ENdeletecontrol(self, index):
        self._reset_error()
        super().ENdeletecontrol(index)
        self._check_for_error()

    def ENdeletecurve(self, indexCurve):
        self._reset_error()
        super().ENdeletecurve(indexCurve)
        self._check_for_error()

    def ENdeletedemand(self, nodeIndex, demandIndex):
        self._reset_error()
        super().ENdeletedemand(nodeIndex, demandIndex)
        self._check_for_error()

    def ENdeletelink(self, indexLink, condition):
        self._reset_error()
        super().ENdeletelink(indexLink, condition)
        self._check_for_error()

    def ENdeletenode(self, indexNode, condition):
        self._reset_error()
        super().ENdeletenode(indexNode, condition)
        self._check_for_error()

    def ENdeletepattern(self, indexPat):
        self._reset_error()
        super().ENdeletepattern(indexPat)
        self._check_for_error()

    def ENdeleteproject(self):
        self._reset_error()
        super().ENdeleteproject()
        self._check_for_error()

    def ENdeleterule(self, index):
        self._reset_error()
        super().ENdeleterule(index)
        self._check_for_error()

    def ENgetaveragepatternvalue(self, index):
        self._reset_error()
        r = super().ENgetaveragepatternvalue(index)
        self._check_for_error()
        return r

    def ENgetbasedemand(self, index, numdemands):
        self._reset_error()
        r = super().ENgetbasedemand(index, numdemands)
        self._check_for_error()
        return r

    def ENgetcomment(self, object_, index):
        self._reset_error()
        r = super().ENgetcomment(object_, index)
        self._check_for_error()
        return r

    def ENgetcontrol(self, cindex):
        self._reset_error()
        r = super().ENgetcontrol(cindex)
        self._check_for_error()
        return r

    def ENgetcoord(self, index):
        self._reset_error()
        r = super().ENgetcoord(index)
        self._check_for_error()
        return r

    def ENgetcount(self, countcode):
        self._reset_error()
        r = super().ENgetcount(countcode)
        self._check_for_error()
        return r

    def ENgetcurve(self, index):
        self._reset_error()
        r = super().ENgetcurve(index)
        self._check_for_error()
        return r

    def ENgetcurveid(self, index):
        self._reset_error()
        r = super().ENgetcurveid(index)
        self._check_for_error()
        return r

    def ENgetcurveindex(self, Id):
        self._reset_error()
        r = super().ENgetcurveindex(Id)
        self._check_for_error()
        return r

    def ENgetcurvelen(self, index):
        self._reset_error()
        r = super().ENgetcurvelen(index)
        self._check_for_error()
        return r

    def ENgetcurvetype(self, index):
        self._reset_error()
        r = super().ENgetcurvetype(index)
        self._check_for_error()
        return r

    def ENgetcurvevalue(self, index, period):
        self._reset_error()
        r = super().ENgetcurvevalue(index, period)
        self._check_for_error()
        return r

    def ENgetdemandindex(self, nodeindex, demandName):
        self._reset_error()
        r = super().ENgetdemandindex(nodeindex, demandName)
        self._check_for_error()
        return r

    def ENgetdemandmodel(self):
        self._reset_error()
        r = super().ENgetdemandmodel()
        self._check_for_error()
        return r

    def ENgetdemandname(self, node_index, demand_index):
        self._reset_error()
        r = super().ENgetdemandname(node_index, demand_index)
        self._check_for_error()
        return r

    def ENgetdemandpattern(self, index, numdemands):
        self._reset_error()
        r = super().ENgetdemandpattern(index,numdemands)
        self._check_for_error()
        return r

    def ENgetelseaction(self, ruleIndex, actionIndex):
        self._reset_error()
        r = super().ENgetelseaction(ruleIndex, actionIndex)
        self._check_for_error()
        return r

    def ENgetflowunits(self):
        self._reset_error()
        r = super().ENgetflowunits()
        self._check_for_error()
        return r

    def ENgetheadcurveindex(self, pumpindex):
        self._reset_error()
        r = super().ENgetheadcurveindex(pumpindex)
        self._check_for_error()
        return r

    def ENgetlinkid(self, index):
        self._reset_error()
        r = super().ENgetlinkid(index)
        self._check_for_error()
        return r

    def ENgetlinkindex(self, Id):
        self._reset_error()
        r = super().ENgetlinkindex(Id)
        self._check_for_error()
        return r

    def ENgetlinknodes(self, index):
        self._reset_error()
        r = super().ENgetlinknodes(index)
        self._check_for_error()
        return r

    def ENgetlinktype(self, index):
        self._reset_error()
        r = super().ENgetlinktype(index)
        self._check_for_error()
        return r

    def ENgetlinkvalue(self, index, paramcode):
        self._reset_error()
        r = super().ENgetlinkvalue(index, paramcode)
        self._check_for_error()
        return r

    def ENgetnodeid(self, index):
        self._reset_error()
        r = super().ENgetnodeid(index)
        self._check_for_error()
        return r

    def ENgetnodeindex(self, Id):
        self._reset_error()
        r = super().ENgetnodeindex(Id)
        self._check_for_error()
        return r

    def ENgetnodetype(self, index):
        self._reset_error()
        r = super().ENgetnodetype(index)
        self._check_for_error()
        return r

    def ENgetnodevalue(self, index, code_p):
        self._reset_error()
        r = super().ENgetnodevalue(index, code_p)
        self._check_for_error()
        return r

    def ENgetnumdemands(self, index):
        self._reset_error()
        r = super().ENgetnumdemands(index)
        self._check_for_error()
        return r

    def ENgetoption(self, optioncode):
        self._reset_error()
        r = super().ENgetoption(optioncode)
        self._check_for_error()
        return r

    def ENgetpatternid(self, index):
        self._reset_error()
        r = super().ENgetpatternid(index)
        self._check_for_error()
        return r

    def ENgetpatternindex(self, Id):
        self._reset_error()
        r = super().ENgetpatternindex(Id)
        self._check_for_error()
        return r

    def ENgetpatternlen(self, index):
        self._reset_error()
        r = super().ENgetpatternlen(index)
        self._check_for_error()
        return r

    def ENgetpatternvalue(self, index, period):
        self._reset_error()
        r = super().ENgetpatternvalue(index, period)
        self._check_for_error()
        return r

    def ENgetpremise(self, ruleIndex, premiseIndex):
        self._reset_error()
        r = super().ENgetpremise(ruleIndex, premiseIndex)
        self._check_for_error()
        return r

    def ENgetpumptype(self, index):
        self._reset_error()
        r = super().ENgetpumptype(index)
        self._check_for_error()
        return r

    def ENgetqualinfo(self):
        self._reset_error()
        r = super().ENgetqualinfo()
        self._check_for_error()
        return r

    def ENgetqualtype(self):
        self._reset_error()
        r = super().ENgetqualtype()
        self._check_for_error()
        return r

    def ENgetresultindex(self, objecttype, index):
        self._reset_error()
        r = super().ENgetresultindex(objecttype, index)
        self._check_for_error()
        return r

    def ENgetrule(self, index):
        self._reset_error()
        r = super().ENgetrule(index)
        self._check_for_error()
        return r

    def ENgetruleID(self, index):
        self._reset_error()
        r = super().ENgetruleID(index)
        self._check_for_error()
        return r

    def ENgetstatistic(self, code):
        self._reset_error()
        r = super().ENgetstatistic(code)
        self._check_for_error()
        return r

    def ENgetthenaction(self, ruleIndex, actionIndex):
        self._reset_error()
        r = super().ENgetthenaction(ruleIndex, actionIndex)
        self._check_for_error()
        return r

    def ENgettimeparam(self, paramcode):
        self._reset_error()
        r = super().ENgettimeparam(paramcode)
        self._check_for_error()
        return r

    def ENgettitle(self):
        self._reset_error()
        r = super().ENgettitle()
        self._check_for_error()
        return r

    def ENgetversion(self):
        self._reset_error()
        r = super().ENgetversion()
        self._check_for_error()
        return r

    def ENgetvertex(self, index, vertex):
        self._reset_error()
        r = super().ENgetvertex(index, vertex)
        self._check_for_error()
        return r

    def ENgetvertexcount(self, index):
        self._reset_error()
        r = super().ENgetvertexcount(index)
        self._check_for_error()
        return r

    def ENinit(self, unitsType, headLossType):
        self._reset_error()
        super().ENinit(unitsType, headLossType)
        self._check_for_error()

    def ENinitH(self, flag):
        self._reset_error()
        super().ENinitH(flag)
        self._check_for_error()

    def ENinitQ(self, saveflag):
        self._reset_error()
        super().ENinitQ(saveflag)
        self._check_for_error()

    def ENnextH(self):
        self._reset_error()
        r = super().ENnextH()
        self._check_for_error()
        return r

    def ENnextQ(self):
        self._reset_error()
        r = super().ENnextQ()
        self._check_for_error()
        return r

    def ENopen(self, inpname=None, repname=None, binname=None):
        self._reset_error()
        super().ENopen(inpname, repname, binname)
        self._check_for_error()

    def ENopenH(self):
        self._reset_error()
        super().ENopenH()
        self._check_for_error()

    def ENopenQ(self):
        self._reset_error()
        super().ENopenQ()
        self._check_for_error()

    def ENreport(self):
        self._reset_error()
        super().ENreport()
        self._check_for_error()

    def ENresetreport(self):
        self._reset_error()
        super().ENresetreport()
        self._check_for_error()

    def ENrunH(self):
        self._reset_error()
        r = super().ENrunH()
        self._check_for_error()
        return r

    def ENrunQ(self):
        self._reset_error()
        r = super().ENrunQ()
        self._check_for_error()
        return r

    def ENsaveH(self):
        self._reset_error()
        super().ENsaveH()
        self._check_for_error()

    def ENsavehydfile(self, fname):
        self._reset_error()
        super().ENsavehydfile(fname)
        self._check_for_error()

    def ENsaveinpfile(self, inpname):
        self._reset_error()
        super().ENsaveinpfile(inpname)
        self._check_for_error()

    def ENsetbasedemand(self, index, demandIdx, value):
        self._reset_error()
        super().ENsetbasedemand(index, demandIdx, value)
        self._check_for_error()

    def ENsetcomment(self, object_, index, comment):
        self._reset_error()
        super().ENsetcomment(object_, index, comment)
        self._check_for_error()

    def ENsetcontrol(self, cindex, ctype, lindex, setting, nindex, level):
        self._reset_error()
        super().ENsetcontrol(cindex, ctype, lindex, setting, nindex, level)
        self._check_for_error()

    def ENsetcoord(self, index, x, y):
        self._reset_error()
        super().ENsetcoord(index, x, y)
        self._check_for_error()

    def ENsetcurve(self, index, x, y, nfactors):
        self._reset_error()
        super().ENsetcurve(index, x, y, nfactors)
        self._check_for_error()

    def ENsetcurveid(self, index, Id):
        self._reset_error()
        super().ENsetcurveid(index, Id)
        self._check_for_error()

    def ENsetcurvevalue(self, index, pnt, x, y):
        self._reset_error()
        super().ENsetcurvevalue(index, pnt, x, y)
        self._check_for_error()

    def ENsetdemandmodel(self, Type, pmin, preq, pexp):
        self._reset_error()
        super().ENsetdemandmodel(Type, pmin, preq, pexp)
        self._check_for_error()

    def ENsetdemandname(self, node_index, demand_index, demand_name):
        self._reset_error()
        super().ENsetdemandname(node_index, demand_index, demand_name)
        self._check_for_error()

    def ENsetdemandpattern(self, index, demandIdx, patInd):
        self._reset_error()
        super().ENsetdemandpattern(index, demandIdx, patInd)
        self._check_for_error()

    def ENsetelseaction(self, ruleIndex, actionIndex, linkIndex, status, setting):
        self._reset_error()
        super().ENsetelseaction(ruleIndex, actionIndex, linkIndex, status, setting)
        self._check_for_error()

    def ENsetflowunits(self, code):
        self._reset_error()
        super().ENsetflowunits(code)
        self._check_for_error()

    def ENsetheadcurveindex(self, pumpindex, curveindex):
        self._reset_error()
        super().ENsetheadcurveindex(pumpindex, curveindex)
        self._check_for_error()

    def ENsetjuncdata(self, index, elev, dmnd, dmndpat):
        self._reset_error()
        super().ENsetjuncdata(index, elev, dmnd, dmndpat)
        self._check_for_error()

    def ENsetlinkid(self, index, newid):
        self._reset_error()
        super().ENsetlinkid(index, newid)
        self._check_for_error()

    def ENsetlinknodes(self, index, startnode, endnode):
        self._reset_error()
        super().ENsetlinknodes(index, startnode, endnode)
        self._check_for_error()

    def ENsetlinktype(self, indexLink, paramcode, actionCode):
        self._reset_error()
        r = super().ENsetlinktype(indexLink, paramcode, actionCode)
        self._check_for_error()
        return r

    def ENsetlinkvalue(self, index, paramcode, value):
        self._reset_error()
        super().ENsetlinkvalue(index, paramcode, value)
        self._check_for_error()

    def ENsetnodeid(self, index, newid):
        self._reset_error()
        super().ENsetnodeid(index, newid)
        self._check_for_error()

    def ENsetnodevalue(self, index, paramcode, value):
        self._reset_error()
        super().ENsetnodevalue(index, paramcode, value)
        self._check_for_error()

    def ENsetoption(self, optioncode, value):
        self._reset_error()
        super().ENsetoption(optioncode, value)
        self._check_for_error()

    def ENsetpattern(self, index, factors, nfactors):
        self._reset_error()
        super().ENsetpattern(index, factors, nfactors)
        self._check_for_error()

    def ENsetpatternid(self, index, Id):
        self._reset_error()
        super().ENsetpatternid(index, Id)
        self._check_for_error()

    def ENsetpatternvalue(self, index, period, value):
        self._reset_error()
        super().ENsetpatternvalue(index, period, value)
        self._check_for_error()

    def ENsetpipedata(self, index, length, diam, rough, mloss):
        self._reset_error()
        super().ENsetpipedata(index, length, diam, rough, mloss)
        self._check_for_error()

    def ENsetpremise(self, ruleIndex, premiseIndex, logop, object_, objIndex, variable,
                     relop, status, value):
        self._reset_error()
        super().ENsetpremise(ruleIndex, premiseIndex, logop, object_, objIndex, variable,
                             relop, status, value)
        self._check_for_error()

    def ENsetpremiseindex(self, ruleIndex, premiseIndex, objIndex):
        self._reset_error()
        super().ENsetpremiseindex(ruleIndex, premiseIndex, objIndex)
        self._check_for_error()

    def ENsetpremisestatus(self, ruleIndex, premiseIndex, status):
        self._reset_error()
        super().ENsetpremisestatus(ruleIndex, premiseIndex, status)
        self._check_for_error()

    def ENsetpremisevalue(self, ruleIndex, premiseIndex, value):
        self._reset_error()
        super().ENsetpremisevalue(ruleIndex, premiseIndex, value)
        self._check_for_error()

    def ENsetqualtype(self, qualcode, chemname, chemunits, tracenode):
        self._reset_error()
        super().ENsetqualtype(qualcode, chemname, chemunits, tracenode)
        self._check_for_error()

    def ENsetreport(self, command):
        self._reset_error()
        super().ENsetreport(command)
        self._check_for_error()

    def ENsetrulepriority(self, ruleIndex, priority):
        self._reset_error()
        super().ENsetrulepriority(ruleIndex, priority)
        self._check_for_error()

    def ENsetstatusreport(self, statuslevel):
        self._reset_error()
        super().ENsetstatusreport(statuslevel)
        self._check_for_error()

    def ENsettankdata(self, index, elev, initlvl, minlvl, maxlvl, diam, minvol, volcurve):
        self._reset_error()
        super().ENsettankdata(index, elev, initlvl, minlvl, maxlvl, diam, minvol, volcurve)
        self._check_for_error()

    def ENsetthenaction(self, ruleIndex, actionIndex, linkIndex, status, setting):
        self._reset_error()
        super().ENsetthenaction(ruleIndex, actionIndex, linkIndex, status, setting)
        self._check_for_error()

    def ENsettimeparam(self, paramcode, timevalue):
        self._reset_error()
        super().ENsettimeparam(paramcode, timevalue)
        self._check_for_error()

    def ENsettitle(self, line1, line2, line3):
        self._reset_error()
        super().ENsettitle(line1, line2, line3)
        self._check_for_error()

    def ENsetvertices(self, index, x, y, vertex):
        self._reset_error()
        super().ENsetvertices(index, x, y, vertex)
        self._check_for_error()

    def ENsolveH(self):
        self._reset_error()
        super().ENsolveH()
        self._check_for_error()

    def ENsolveQ(self):
        self._reset_error()
        super().ENsolveQ()
        self._check_for_error()

    def ENstepQ(self):
        self._reset_error()
        r = super().ENstepQ()
        self._check_for_error()
        return r

    def ENusehydfile(self, hydfname):
        self._reset_error()
        super().ENusehydfile(hydfname)
        self._check_for_error()

    def ENwriteline(self, line):
        self._reset_error()
        super().ENwriteline(line)
        self._check_for_error()
