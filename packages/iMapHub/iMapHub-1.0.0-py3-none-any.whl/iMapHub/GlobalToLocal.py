from databricks.sdk.runtime import *
import pandas as pd
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("abc").getOrCreate()

class InvalidEntryEnteredError(Exception):
  def __init__(self,message,df):
    self.message = message
    super().__init__(self.message,df)
    
class MountPointNotConfiguredError(Exception):
  def __init__(self,message):
    self.message = message
    super().__init__(self.message)

def GetMappedData(groupName, hierarchyName, grainLevel, environment):

    df_parquet = spark.read.format("parquet").load("/mnt/adls/Unilever/ManualConfig/parquet")
    df_pd = df_parquet.toPandas()

    if df_pd[df_pd['HierarchyGroupName'].str.fullmatch(f"{groupName}",case=False) 
             & df_pd['TargetHierarchyName'].str.fullmatch(f"{hierarchyName}",case=False) 
             & df_pd['GrainLevel'].str.fullmatch(f"{grainLevel}",case=False) 
             & df_pd['GrainLevel'].str.fullmatch(f"{grainLevel}",case=False)
             & df_pd['Environment'].str.contains(f"{environment}",case=False)].empty == True:
        
        raise InvalidEntryEnteredError(f"invalid entries entered, suggested entries are above", print(df_pd[["HierarchyGroupName", "TargetHierarchyName", "GrainLevel", "Environment"]]))
    
    else:
        df_pd = df_pd[df_pd['HierarchyGroupName'].str.fullmatch(f"{groupName}",case=False) 
                & df_pd['TargetHierarchyName'].str.fullmatch(f"{hierarchyName}",case=False) 
                & df_pd['GrainLevel'].str.fullmatch(f"{grainLevel}",case=False) 
                & df_pd['GrainLevel'].str.fullmatch(f"{grainLevel}",case=False)
                & df_pd['Environment'].str.contains(f"{environment}",case=False)] 

    local_cols = df_pd['TargetAttributes_Tgt'].iloc[0]
    local_split_cols = local_cols.split(", ")
    local_prefixed_cols = ["Tgt." + sub for sub in local_split_cols] 
    final_local_cols = ', '.join(local_prefixed_cols)

    global_cols = df_pd['SourceAttributes_Src'].iloc[0]
    global_split_cols = global_cols.split(", ")
    global_prefixed_cols = ["Src." + sub for sub in global_split_cols] 
    final_global_cols = ', '.join(global_prefixed_cols)

    if environment.casefold() == 'PROD'.casefold():
        adls = 'dbstorageda18p80049adls'
    elif environment.casefold() == 'UAT'.casefold():
        adls = 'dbstorageda19b80158adls'
    elif environment.casefold() == 'DEV'.casefold():
        adls = 'dbstorageda22d80046adls'

    df_mounts = dbutils.fs.mounts()
    df_mount_pd = pd.DataFrame(df_mounts)
    if df_mount_pd[df_mount_pd['source'].str.contains(f"unilever@{adls}.dfs.core.windows.net/$",case=False)].empty == False  :
        mntpoint = df_mount_pd[df_mount_pd['source'].str.contains(f"unilever@{adls}.dfs.core.windows.net/$",case=False)]['mountPoint'].iloc[0]
        initialpath = "None"
    elif df_mount_pd[df_mount_pd['source'].str.contains(f"unilever@{adls}.dfs.core.windows.net.*/BusinessDataLake/$",case=False)].empty == False :
        mntpoint = df_mount_pd[df_mount_pd['source'].str.contains(f"unilever@{adls}.dfs.core.windows.net.*/BusinessDataLake/$",case=False)]['mountPoint'].iloc[0]
        initialpath = "/BusinessDataLake"
    elif df_mount_pd[df_mount_pd['source'].str.contains(f"unilever@{adls}.dfs.core.windows.net.*/BusinessDataLake/SC/$",case=False)].empty == False :
        mntpoint = df_mount_pd[df_mount_pd['source'].str.contains(f"unilever@{adls}.dfs.core.windows.net.*/BusinessDataLake/SC/$",case=False)]['mountPoint'].iloc[0]
        initialpath = "/BusinessDataLake/SC"
    else:
        raise MountPointNotConfiguredError(f"MountPoint is not configured for the following storage account:{adls}({environment}), please connect with the Landscape Team")
    
    local_path = df_pd['TargetPhysicalPath'].iloc[0]
    final_local_path = local_path.replace(initialpath, '')
    complete_local_path = mntpoint + final_local_path

    global_path = df_pd['SourcePhysicalPath'].iloc[0]
    final_global_path = global_path.replace(initialpath, '')
    complete_global_path = mntpoint + final_global_path

    join_condition = df_pd['JoinCondition'].iloc[0]

    df_bdl_global = spark.read.format("delta").load(complete_global_path)
    df_bdl_global.createOrReplaceTempView('vw_bdl_hgpl')

    data_local = spark.read.format("delta").load(complete_local_path)
    data_local.createOrReplaceTempView('vw_udl_local')
    
    df = spark.sql(f"""Select {final_global_cols}, {final_local_cols},  Tgt.* except({local_cols})
                  from vw_bdl_hgpl as Src inner join vw_udl_local as Tgt  
                  ON {join_condition}""")
    return df
