# Pr_crawle

数据库信息在 `pr\mysqlpipelines\sql.py` 修改

数据库表
```
DROP TABLE IF EXISTS `dd_name`;
CREATE TABLE `dd_name` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `xs_name` varchar(255) DEFAULT NULL,
  `xs_author` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `name_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;
```

```
DROP TABLE IF EXISTS `dd_chaptername`;
CREATE TABLE `dd_chaptername` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `xs_chaptername` varchar(255) DEFAULT NULL,
  `xs_content` text,
  `id_name` int(11) DEFAULT NULL,
  `num_id` int(11) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=gb18030;
SET FOREIGN_KEY_CHECKS=1;
```
