import numpy as _np
import os as _os
import emcpy.dateutils as _dateutils
import emcpy.io as _io

def obspace_stats(datapath,date1,date2,expt_names,n_mem,ob_types=["u"],codes_uv=[187],codes_tq=[287],\
                        p_max=1050.0,p_min=100.0,lat_max=90.0,lat_min=0.0,lon_max=360.0,lon_min=0.0,\
                        error_max=40.0,error_min=0.000001):
    """
    Computes observation space stats into 3D arrays (n_ob_type, n_expt, 24) and plots the stats as a
    function of hour of day.

    Args:
      datapath   : (str) netCDF filename 
      date1      : (str "YYYYMMDDHH") start date
      date2      : (str "YYYYMMDDHH") end date
      expt_names : (list of str) experiment names
      n_mem      : (int) number of ensemble members
      ob_types   : (list of str) observation types (u,v,t,q,etc.)
      codes_uv   : (list of int) uv bufr codes used to filter obs
      codes_tq   : (list of int) tq bufr codes used to filter obs
      p_max      : (float) maximum pressure (mb) for including observation in calculations
      p_min      : (float) minimum pressure (mb) for including observation in calculations
      lat_max    : (float) maximum latitude (deg N) for including observation in calculations
      lat_min    : (float) minimum latitude (deg N) for including observation in calculations
      lon_max    : (float) maximum latitude (deg E) for including observation in calculations
      lon_min    : (float) minimum latitude (deg E) for including observation in calculations
      error_max  : (float) maximum error standard deviation for including observation in calculations
      error_min  : (float) minimum error standard deviation for including observation in calculations

    Returns:
      dates         : (list str) list of date strings of the form YYYYMMDDHH based on date1 and date2
      bias          : (array float) mean of (forecast - observation)
      rms           : (array float) rms of (F-O)
      std_dev       : (array float) standard deviation of (F-O)
      rmse          : (array float) total spread (standard deviation)
      spread        : (array float) ensemble spread (standard deviation)
      ob_error      : (array float) observation error standard deviation
      total_spread  : (array float) rms of (O-Omf) = rmse of ensemble mean fcst
      num_obs_total : (array float) total number of observations
      num_obs_assim : (array float) total number of observations assimilated
      cr            : (array float) consistency ratio (total spread/rmsi)**2
      ser           : (array float) spread error ratio (intraensemble std_dev/ rmse of ensemble mean fcst)

    References:
        consistency ratio (cr)
          a) https://journals.ametsoc.org/view/journals/atot/26/5/2008jtecha1156_1.xml (eq 3.4)
          b) https://journals.ametsoc.org/view/journals/mwre/150/8/MWR-D-21-0289.1.xml (eq 7)
        spread error ratio (ser)
          a) https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2013GL057630 (eq 1)
        bufr codes
          a) https://emc.ncep.noaa.gov/mmb/data_processing/prepbufr.doc/table_2.htm
    """

    hours=24
    dates=_dateutils.daterange(date1,date2,1)
    n_expt=len(expt_names)
    n_ob_type=len(ob_types)
    bias         =_np.zeros(shape=(n_ob_type,n_expt,24))
    rms          =_np.zeros(shape=(n_ob_type,n_expt,24))
    std_dev      =_np.zeros(shape=(n_ob_type,n_expt,24))
    rmse         =_np.zeros(shape=(n_ob_type,n_expt,24))
    spread       =_np.zeros(shape=(n_ob_type,n_expt,24))
    total_spread =_np.zeros(shape=(n_ob_type,n_expt,24))
    ob_error     =_np.zeros(shape=(n_ob_type,n_expt,24))
    num_obs_assim=_np.zeros(shape=(n_ob_type,n_expt,24))
    num_obs_total=_np.zeros(shape=(n_ob_type,n_expt,24))
    cr           =_np.zeros(shape=(n_ob_type,n_expt,24))
    ser          =_np.zeros(shape=(n_ob_type,n_expt,24))

    sum_innov       =_np.zeros(24)
    sum_innovsq     =_np.zeros(24)
    sum_fcst_ens_var=_np.zeros(24)
    sum_ob_err_var  =_np.zeros(24)

    for date in dates:
      times = _dateutils.datetohrs(date)
      pdy=str(date[0:8])
      hour=int(str(date[8:10]))
      if(hour<=18):
        continue #As of right now, the rrfs only runs the EnKF at 18-23Z so skip those off times
      for ob_type in ob_types:
        i_o=ob_types.index(ob_type)
        for expt_name in expt_names:
          print("%s %s %s" % (date,expt_name,ob_type))
          i_e=expt_names.index(expt_name)
          mem=1
          while(mem <= n_mem):
            memid=str(mem).zfill(4)
            if(ob_type == "u" or ob_type == "v"):
              obsfile=_os.path.join(datapath,'%s/%s/mem%s/diag_conv_uv_ges.%s.nc4' % (expt_name,date,memid,date))
            else:
              obsfile=_os.path.join(datapath,'%s/%s/mem%s/diag_conv_%s_ges.%s.nc4' % (expt_name,date,memid,ob_type,date))

            if(mem == 1):
              code    =_io.netCDF.read_netCDF_var(obsfile,'Observation_Type',oneD=True)
              lat     =_io.netCDF.read_netCDF_var(obsfile,'Latitude',oneD=True)
              lon     =_io.netCDF.read_netCDF_var(obsfile,'Longitude',oneD=True)
              pressure=_io.netCDF.read_netCDF_var(obsfile,'Pressure',oneD=True)
              use     =_io.netCDF.read_netCDF_var(obsfile,'Analysis_Use_Flag',oneD=True)
              errorinv=_io.netCDF.read_netCDF_var(obsfile,'Errinv_Final',oneD=True)

              #https://emc.ncep.noaa.gov/mmb/data_processing/prepbufr.doc/table_2.htm
              if(ob_type == "u" or ob_type == "v"):
                codes=codes_uv
              elif(ob_type == "t" or ob_type == "q"):
                codes=codes_tq


              if(ob_type == "u"):
                ob=_io.netCDF.read_netCDF_var(obsfile,'u_Observation',oneD=True)
              elif(ob_type == "v"):
                ob=_io.netCDF.read_netCDF_var(obsfile,'v_Observation',oneD=True)
              else:
                ob=_io.netCDF.read_netCDF_var(obsfile,'Observation',oneD=True)
    
              if(ob_type == "q"):
                ob=1000.0*ob #convert from kg/kg to g/kg
                errorinv=errorinv/1000.0 #convert from kg/kg to g/kg

              #consider where use flag==1 and bound by error/lat/lon/pres 
              used = _io.netCDF.filter_obs(code,codes,errorinv,lat,lon,pressure,\
                                      use=1,p_max=p_max,p_min=p_min,lat_max=lat_max,lat_min=lat_min,\
                                      lon_max=lon_max,lon_min=lon_min,error_max=error_max,error_min=error_min)

              errorinv=errorinv[used]
              error=1.0/errorinv
              itot=len(ob)
              ob=ob[used]
              iasm=len(ob)

              #end if mem==1
  
            if(ob_type == "u"):
              omf=_io.netCDF.read_netCDF_var(obsfile,'u_Obs_Minus_Forecast_adjusted',oneD=True)
            elif(ob_type == "v"):
              omf=_io.netCDF.read_netCDF_var(obsfile,'v_Obs_Minus_Forecast_adjusted',oneD=True)
            else:
              omf=_io.netCDF.read_netCDF_var(obsfile,'Obs_Minus_Forecast_adjusted',oneD=True)
            if(ob_type == "q"):
              omf=1000.0*omf #convert from kg/kg to g/kg
  
            omf=omf[used]
         
            if(mem == 1):
               fcst_ens_mean = ob - omf
               fcst_ens_var = (ob - omf)**2
            else:
               fcst_ens_mean = fcst_ens_mean + ob - omf
               fcst_ens_var = fcst_ens_var + (ob - omf)**2
            mem=mem+1
            #end while n_mem
  
          error_var=error**2
          fcst_ens_mean=fcst_ens_mean/n_mem
          if(n_mem > 1):
            fcst_ens_var  = (fcst_ens_var - n_mem*fcst_ens_mean**2) / (n_mem - 1)
          else:
            fcst_ens_var = 0.0
          innov = ob - fcst_ens_mean
          num_obs_total[i_o,i_e,hour]=num_obs_total[i_o,i_e,hour]+itot
          num_obs_assim[i_o,i_e,hour]=num_obs_assim[i_o,i_e,hour]+iasm
          sum_innov[hour]       =sum_innov[hour]       +_np.sum(innov)
          sum_innovsq[hour]     =sum_innovsq[hour]     +_np.sum(innov**2)
          sum_fcst_ens_var[hour]=sum_fcst_ens_var[hour]+_np.sum(fcst_ens_var)
          sum_ob_err_var[hour]  =sum_ob_err_var[hour]  +_np.sum(error_var)
  
          #end n_times
  
          if(num_obs_assim[i_o,i_e,hour] > 0):
            mean_innov            = sum_innov[hour] / num_obs_assim[i_o,i_e,hour]
            bias[i_o,i_e,hour]    = -1*mean_innov 
            rms[i_o,i_e,hour]     = _np.sqrt(sum_innovsq[hour]/num_obs_assim[i_o,i_e,hour])
            mean_ob_err_var       = sum_ob_err_var[hour] / num_obs_assim[i_o,i_e,hour]
            ob_error[i_o,i_e,hour]= _np.sqrt(mean_ob_err_var)
            rmse[i_o,i_e,hour]    = _np.sqrt(sum_fcst_ens_var[hour]/num_obs_assim[i_o,i_e,hour]) 
  
          if(num_obs_assim[i_o,i_e,hour] > 1):
            innov_var=(sum_innovsq[hour]-num_obs_assim[i_o,i_e,hour]*mean_innov**2)/(num_obs_assim[i_o,i_e,hour]-1.0)
            std_dev[i_o,i_e,hour]     =_np.sqrt(innov_var)
            mean_fcst_var             =sum_fcst_ens_var[hour] / num_obs_assim[i_o,i_e,hour]
            spread[i_o,i_e,hour]      =_np.sqrt(mean_fcst_var)
            total_spread[i_o,i_e,hour]=_np.sqrt(mean_ob_err_var + mean_fcst_var)
            cr[i_o,i_e,hour]          =(total_spread[i_o,i_e,hour]/rms[i_o,i_e,hour])**2
            ser[i_o,i_e,hour]         =spread[i_o,i_e,hour]/rmse[i_o,i_e,hour]

        #end do n_expt
      #end do n_ob_type

    return dates,bias,rms,std_dev,rmse,spread,ob_error,total_spread,num_obs_total,num_obs_assim,cr,ser
