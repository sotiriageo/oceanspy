import pytest
import xarray as xr
import numpy as np
import pandas as pd
from oceanspy import OceanDataset

class Datasets:
    def __init__(self):
        # Create a small datasets
        self.NX = 9
        self.NY = 10
        self.NZ = 11
        self.NT = 12
        
    def sinusoidal(self):
        
        moreval = 1
        step    = 0.1
        
        # Horizontal Dimensions
        X      = xr.DataArray( np.arange(self.NX*moreval),       dims = 'X')  * step
        Xp1    = xr.DataArray( np.arange(self.NX*moreval+1)-0.5, dims = 'Xp1')* step
        Y      = xr.DataArray( np.arange(self.NY*moreval),       dims = 'Y')  * step
        Yp1    = xr.DataArray( np.arange(self.NY*moreval+1)-0.5, dims = 'Yp1')* step
        
        # Vertical Dimensions
        Z      = xr.DataArray(-np.arange(self.NZ*moreval)-0.5, dims = 'Z')  * step
        Zp1    = xr.DataArray(-np.arange(self.NZ*moreval+1),   dims = 'Zp1')* step
        Zu     = xr.DataArray(-np.arange(self.NZ*moreval)-1,   dims = 'Zu') * step
        Zl     = xr.DataArray(-np.arange(self.NZ*moreval),     dims = 'Zl') * step
        
        # Space Coordinates
        YC, XC = xr.broadcast(Y,   X)
        YG, XG = xr.broadcast(Yp1, Xp1)
        YU, XU = xr.broadcast(Y  , Xp1)
        YV, XV = xr.broadcast(Yp1, X)
        
        # Spacing
        drC = xr.full_like(Zp1, step)
        drF = xr.full_like(Z  , step)
        dxC = xr.full_like(XU,  step)
        dyC = xr.full_like(XV,  step)
        dxF = xr.full_like(XC,  step)
        dyF = xr.full_like(XC,  step)
        dxG = xr.full_like(XV,  step)
        dyG = xr.full_like(XU,  step)
        dxV = xr.full_like(XG,  step)
        dyU = xr.full_like(XG,  step)
        
        # Areas
        rA  = dxF * dyF
        rAw = dxC * dyG
        rAs = dxG * dyC 
        rAz = dxV * dyU 

        # HFac
        HFacC, _ = xr.broadcast(xr.full_like(Z, 1), xr.full_like(XC, 1))
        HFacW, _ = xr.broadcast(xr.full_like(Z, 1), xr.full_like(XU, 1))
        HFacS, _ = xr.broadcast(xr.full_like(Z, 1), xr.full_like(XV, 1))
        
        # Sin C points
        sinZ, sinY, sinX = xr.broadcast(np.sin(Z), np.sin(Y), np.sin(X))
        
        # Sin vel points
        sinUZ, sinUY , sinUX = xr.broadcast(np.sin(Z) , np.sin(Y)  , np.sin(Xp1))
        sinVZ, sinVY , sinVX = xr.broadcast(np.sin(Z) , np.sin(Yp1), np.sin(X))
        sinWZ, sinWY , sinWX = xr.broadcast(np.sin(Zl), np.sin(Y)  , np.sin(X))
        

        return xr.Dataset({'X'     : X,      'Xp1'   : Xp1, 
                           'Y'     : Y,      'Yp1'   : Yp1,
                           'Z'     : Z,      'Zp1'   : Zp1, 'Zu': Zu, 'Zl': Zl,
                           'YC'    : YC,     'XC'    : XC, 
                           'YG'    : YG,     'XG'    : XG, 
                           'YU'    : YU,     'XU'    : XU, 
                           'YV'    : YV,     'XV'    : XV,
                           'drC'   : drC,    'drF'   : drF,
                           'dxC'   : dxC,    'dyC'   : dyC,
                           'dxF'   : dxF,    'dyF'   : dyF,
                           'dxG'   : dxG,    'dyG'   : dyG,
                           'dxV'   : dxV,    'dyU'   : dyU,
                           'rA'    : rA,     'rAw'   : rAw,
                           'rAs'   : rAs,    'rAz'   : rAz,
                           'HFacC' : HFacC,  'HFacW' : HFacW, 'HFacS' : HFacS,
                           'sinZ'  : sinZ,   'sinY'  : sinY,  'sinX'  : sinX,
                           'sinUZ' : sinUZ,  'sinUY' : sinUY, 'sinUX' : sinUX,
                           'sinVZ' : sinVZ,  'sinVY' : sinVY, 'sinVX' : sinVX,
                           'sinWZ' : sinWZ,  'sinWY' : sinWY, 'sinWX' : sinWX})
        
    def MITgcm_rect_nc(self):
        """
        Similar to exp_ASR and exp_ERAI
        """
        
        # Horizontal Dimensions
        X      = xr.DataArray( np.arange(self.NX),     dims = 'X')
        Xp1    = xr.DataArray( np.arange(self.NX+1),   dims = 'Xp1')
        Y      = xr.DataArray( np.arange(self.NY),     dims = 'Y')
        Yp1    = xr.DataArray( np.arange(self.NY+1),   dims = 'Yp1')
        
        # Vertical Dimensions
        Z      = xr.DataArray(-np.arange(self.NZ)-0.5, dims = 'Z')
        Zp1    = xr.DataArray(-np.arange(self.NZ+1),   dims = 'Zp1')
        Zu     = xr.DataArray(-np.arange(self.NZ)-1,   dims = 'Zu')
        Zl     = xr.DataArray(-np.arange(self.NZ),     dims = 'Zl')

        # Space Coordinates
        YC, XC = xr.broadcast(Y+0.5, X+0.5)
        YG, XG = xr.broadcast(Yp1  , Xp1)
        YU, XU = xr.broadcast(Y+0.5, Xp1)
        YV, XV = xr.broadcast(Yp1  , X+0.5)

        # Time Dimension
        time   = xr.DataArray(pd.date_range('2000-01-01', freq='M', periods=self.NT), dims = 'time')
        
        # Add some nan due to exch2
        rX = np.random.randint(self.NX)
        rY = np.random.randint(self.NY)
        maskC = xr.where(np.logical_or(XC!=XC.isel(X=rX, Y=rY), YC!=YC.isel(X=rX, Y=rY)), 1, 0)
        maskG = xr.where(np.logical_or(XG!=XG.isel(Xp1=rX, Yp1=rY), YG!=YG.isel(Xp1=rX, Yp1=rY)), 1, 0)
        maskU = xr.where(np.logical_or(XU!=XU.isel(Xp1=rX, Y=rY), YU!=YU.isel(Xp1=rX, Y=rY)), 1, 0)
        maskV = xr.where(np.logical_or(XV!=XV.isel(X=rX, Yp1=rY), YV!=YV.isel(X=rX, Yp1=rY)), 1, 0)
        XC = XC.where(maskC); YC = YC.where(maskC)
        XG = XG.where(maskG); YG = YG.where(maskG)
        XU = XU.where(maskU); YU = YU.where(maskU)
        XV = XV.where(maskV); YV = YV.where(maskV)
        
        return xr.Dataset({'X'   : X,    'Xp1': Xp1, 
                           'Y'   : Y,    'Yp1': Yp1,
                           'Z'   : Z,    'Zp1': Zp1, 'Zu': Zu, 'Zl': Zl,
                           'YC'  : YC,   'XC' : XC, 
                           'YG'  : YG,   'XG' : XG, 
                           'YU'  : YU,   'XU' : XU, 
                           'YV'  : YV,   'XV' : XV,
                           'time': time, })
    
    def MITgcm_rect_bin(self):
        """
        Similar to exp_ASR and exp_ERAI
        """
        
        # Horizontal Dimensions
        X      = xr.DataArray( np.arange(self.NX),  dims = 'X')
        Xp1    = xr.DataArray( np.arange(self.NX),  dims = 'Xp1')
        Y      = xr.DataArray( np.arange(self.NY),  dims = 'Y')
        Yp1    = xr.DataArray( np.arange(self.NY),  dims = 'Yp1')
        
        # Vertical Dimensions
        Z      = xr.DataArray(-np.arange(self.NZ)-0.5, dims = 'Z')
        Zp1    = xr.DataArray(-np.arange(self.NZ+1),   dims = 'Zp1')
        Zu     = xr.DataArray(-np.arange(self.NZ)-1,   dims = 'Zu')
        Zl     = xr.DataArray(-np.arange(self.NZ),     dims = 'Zl')

        # Space Coordinates
        YC, XC = xr.broadcast(Y+0.5, X+0.5)
        YG, XG = xr.broadcast(Yp1  , Xp1)
        YU, XU = xr.broadcast(Y+0.5, Xp1)
        YV, XV = xr.broadcast(Yp1  , X+0.5)

        # Time Dimension
        time   = xr.DataArray(pd.date_range('2000-01-01', freq='M', periods=self.NT), dims = 'time')
        
        # Add some nan due to exch2
        rX = np.random.randint(self.NX)
        rY = np.random.randint(self.NY)
        maskC = xr.where(np.logical_or(XC!=XC.isel(X=rX, Y=rY), YC!=YC.isel(X=rX, Y=rY)), 1, 0)
        maskG = xr.where(np.logical_or(XG!=XG.isel(Xp1=rX, Yp1=rY), YG!=YG.isel(Xp1=rX, Yp1=rY)), 1, 0)
        maskU = xr.where(np.logical_or(XU!=XU.isel(Xp1=rX, Y=rY), YU!=YU.isel(Xp1=rX, Y=rY)), 1, 0)
        maskV = xr.where(np.logical_or(XV!=XV.isel(X=rX, Yp1=rY), YV!=YV.isel(X=rX, Yp1=rY)), 1, 0)
        XC = XC.where(maskC); YC = YC.where(maskC)
        XG = XG.where(maskG); YG = YG.where(maskG)
        XU = XU.where(maskU); YU = YU.where(maskU)
        XV = XV.where(maskV); YV = YV.where(maskV)
        
        return xr.Dataset({'X'   : X,    'Xp1': Xp1, 
                           'Y'   : Y,    'Yp1': Yp1,
                           'Z'   : Z,    'Zp1': Zp1, 'Zu': Zu, 'Zl': Zl,
                           'YC'  : YC,   'XC' : XC, 
                           'YG'  : YG,   'XG' : XG, 
                           'YU'  : YU,   'XU' : XU, 
                           'YV'  : YV,   'XV' : XV,
                           'time': time, })
    
    def MITgcm_curv_nc(self):
        """
        Similar to exp_Arctic_Control
        """
        
        # Horizontal Dimensions (use xarray tutorial)
        try:
            ds  = xr.tutorial.open_dataset('rasm')
        except AttributeError:
            # Xarray<0.11
            ds  = xr.tutorial.load_dataset('rasm')
        ds['xc'] = xr.where(ds['xc']>180, ds['xc']-180, ds['xc'])
        X   = ds['x'].isel(x=slice(self.NX)).values
        Xp1 = ds['x'].isel(x=slice(self.NX+1)).values
        Y   = ds['y'].isel(y=slice(self.NY)).values
        Yp1 = ds['y'].isel(y=slice(self.NY+1)).values
        XG  = ds['xc'].isel(x=slice(self.NX+1), y=slice(self.NY+1)).values
        YG  = ds['yc'].isel(x=slice(self.NX+1), y=slice(self.NY+1)).values
        XC  = (XG[:-1, :-1] + XG[1:, 1:])/2
        YC  = (YG[:-1, :-1] + YG[1:, 1:])/2
        
        # Set DataArray
        X      = xr.DataArray( X,   dims = 'X')
        Xp1    = xr.DataArray( Xp1, dims = 'Xp1')
        Y      = xr.DataArray( Y,   dims = 'Y')
        Yp1    = xr.DataArray( Yp1, dims = 'Yp1')
        XC     = xr.DataArray( XC,  dims = ('Y'  , 'X'))
        XG     = xr.DataArray( XG,  dims = ('Yp1', 'Xp1'))
        YC     = xr.DataArray( YC,  dims = ('Y'  , 'X'))
        YG     = xr.DataArray( YG,  dims = ('Yp1', 'Xp1'))
        
        # Vertical Dimensions
        Z      = xr.DataArray(-np.arange(self.NZ)-0.5, dims = 'Z')
        Zp1    = xr.DataArray(-np.arange(self.NZ+1),   dims = 'Zp1')
        Zu     = xr.DataArray(-np.arange(self.NZ)-1,   dims = 'Zu')
        Zl     = xr.DataArray(-np.arange(self.NZ),     dims = 'Zl')
        
        # Time Dimension
        time   = xr.DataArray(pd.date_range('2000-01-01', freq='M', periods=self.NT), dims = 'time')
        
        return xr.Dataset({'X'   : X,    'Xp1': Xp1, 
                           'Y'   : Y,    'Yp1': Yp1,
                           'Z'   : Z,    'Zp1': Zp1, 'Zu': Zu, 'Zl': Zl,
                           'YC'  : YC,   'XC' : XC, 
                           'YG'  : YG,   'XG' : XG, 
                           'time': time, })
    
    
datasets = {'MITgcm_rect_nc' : Datasets().MITgcm_rect_nc(),
            'MITgcm_rect_bin': Datasets().MITgcm_rect_bin(),
            'MITgcm_curv_nc' : Datasets().MITgcm_curv_nc()}

oceandatasets = {'MITgcm_rect_nc' : OceanDataset(datasets['MITgcm_rect_nc']).import_MITgcm_rect_nc(),
                 'MITgcm_rect_bin': OceanDataset(datasets['MITgcm_rect_bin']).import_MITgcm_rect_bin(),
                 'MITgcm_curv_nc' : OceanDataset(datasets['MITgcm_curv_nc']).import_MITgcm_curv_nc()}

aliased_ods = {}
for od_name in oceandatasets:
    dataset = oceandatasets[od_name].dataset
    aliases = {var: 'alias_'+var for var in dataset.variables}
    dataset = dataset.rename(aliases)
    aliased_ods[od_name] = OceanDataset(dataset).set_aliases(aliases)

    
sin_od = OceanDataset(Datasets().sinusoidal()).set_grid_coords({'Y'    : {'Y': None, 'Yp1': 0.5},
                                                                'X'    : {'X': None, 'Xp1': 0.5},
                                                                'Z'    : {'Z': None, 'Zp1': 0.5, 'Zu': 0.5, 'Zl': -0.5}})


MITgcmVarDims = {
                'Z': ['Z'],
                'Zp1': ['Zp1'],
                'Zu': ['Zu'],
                'Zl': ['Zl'],
                'drC': ['Zp1'],
                'drF': ['Z'],
                'X': ['X'],
                'Y': ['Y'],
                'XC': ['Y', 'X'],
                'YC': ['Y', 'X'],
                'Xp1': ['Xp1'],
                'XU': ['Y', 'Xp1'],
                'YU': ['Y', 'Xp1'],
                'Yp1': ['Yp1'],
                'XV': ['Yp1', 'X'],
                'YV': ['Yp1', 'X'],
                'XG': ['Yp1', 'Xp1'],
                'YG': ['Yp1', 'Xp1'],
                'dxC': ['Y', 'Xp1'],
                'dyC': ['Yp1', 'X'],
                'dxF': ['Y', 'X'],
                'dyF': ['Y', 'X'],
                'dxG': ['Yp1', 'X'],
                'dyG': ['Y', 'Xp1'],
                'dxV': ['Yp1', 'Xp1'],
                'dyU': ['Yp1', 'Xp1'],
                'rA': ['Y', 'X'],
                'rAw': ['Y', 'Xp1'],
                'rAs': ['Yp1', 'X'],
                'rAz': ['Yp1', 'Xp1'],
                'fCori': ['Y', 'X'],
                'fCoriG': ['Yp1', 'Xp1'],
                'R_low': ['Y', 'X'],
                'Ro_surf': ['Y', 'X'],
                'Depth': ['Y', 'X'],
                'HFacC': ['Z', 'Y', 'X'],
                'HFacW': ['Z', 'Y', 'Xp1'],
                'HFacS': ['Z', 'Yp1', 'X'],
                'KPPGHAT': ['Z', 'Y', 'X'],
                'KPPHBL': ['Y', 'X'],
                'KPPdiffKzS': ['Z', 'Y', 'X'],
                'KPPdiffKzT': ['Z', 'Y', 'X'],
                'KPPviscAz': ['Z', 'Y', 'X'],
                'EXFaqh': ['time', 'Y', 'X'],
                'EXFatemp': ['time', 'Y', 'X'],
                'EXFempmr': ['time', 'Y', 'X'],
                'EXFevap': ['time', 'Y', 'X'],
                'EXFhl': ['time', 'Y', 'X'],
                'EXFhs': ['time', 'Y', 'X'],
                'EXFlwnet': ['time', 'Y', 'X'],
                'EXFpreci': ['time', 'Y', 'X'],
                'EXFpress': ['time', 'Y', 'X'],
                'EXFqnet': ['time', 'Y', 'X'],
                'EXFroff': ['time', 'Y', 'X'],
                'EXFroft': ['time', 'Y', 'X'],
                'EXFsnow': ['time', 'Y', 'X'],
                'EXFswnet': ['time', 'Y', 'X'],
                'EXFtaux': ['time', 'Y', 'X'],
                'EXFtauy': ['time', 'Y', 'X'],
                'EXFuwind': ['time', 'Y', 'X'],
                'EXFvwind': ['time', 'Y', 'X'],
                'time': ['time'],
                'Eta': ['time', 'Y', 'X'],
                'S': ['time', 'Z', 'Y', 'X'],
                'Temp': ['time', 'Z', 'Y', 'X'],
                'U': ['time', 'Z', 'Y', 'Xp1'],
                'V': ['time', 'Z', 'Yp1', 'X'],
                'W': ['time', 'Zl', 'Y', 'X'],
                'KPPhbl': ['time', 'Y', 'X'],
                'MXLDEPTH': ['time', 'Y', 'X'],
                'RHOAnoma': ['time', 'Z', 'Y', 'X'],
                'SIarea': ['time', 'Y', 'X'],
                'SIheff': ['time', 'Y', 'X'],
                'SIhsnow': ['time', 'Y', 'X'],
                'SIhsalt': ['time', 'Y', 'X'],
                'SIuice': ['time', 'Y', 'Xp1'],
                'SIvice': ['time', 'Yp1', 'X'],
                'TRELAX': ['time', 'Y', 'X'],
                'SRELAX': ['time', 'Y', 'X'],
                'momVort3': ['time', 'Z', 'Yp1', 'Xp1'],
                'oceTAUX': ['time', 'Y', 'Xp1'],
                'oceTAUY': ['time', 'Yp1', 'X'],
                'oceFWflx': ['time', 'Y', 'X'],
                'oceSflux': ['time', 'Y', 'X'],
                'oceQnet': ['time', 'Y', 'X'],
                'oceQsw': ['time', 'Y', 'X'],
                'oceFreez': ['time', 'Y', 'X'],
                'oceSPflx': ['time', 'Y', 'X'],
                'oceSPDep': ['time', 'Y', 'X'],
                'phiHyd': ['time', 'Z', 'Y', 'X'],
                'phiHydLow': ['time', 'Y', 'X'],
                'surForcT': ['time', 'Y', 'X'],
                'surForcS': ['time', 'Y', 'X'],
                'time_midp': ['time_midp'],
                'AngleCS':   ['Y', 'X'],
                'AngleSN':   ['Y', 'X'],}
