
ALTER 
TABLE `libro`

    CHANGE 
`descripcion`
`descripcion`
text 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci DEFAULT
NULL ;
ALTER TABLE libro ADD COLUMN descripcion TEXT;