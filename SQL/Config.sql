use DWH

GO
delete Config where ParamName in ('1C_USER','1C_PASSWORD');

GO
INSERT INTO dbo.Config(
   ParamName
  ,ParamValue
  ,Comment
) VALUES (
   '1C_USER'  -- ParamName - varchar(255)
  ,'user'  -- ParamValue - varchar(2000)
  ,'1c'  -- Comment - varchar(255)
);

GO

INSERT INTO dbo.Config(
   ParamName
  ,ParamValue
  ,Comment
) VALUES (
   '1C_PASSWORD'  -- ParamName - varchar(255)
  ,'pass'  -- ParamValue - varchar(2000)
  ,'1c'  -- Comment - varchar(255)
);


