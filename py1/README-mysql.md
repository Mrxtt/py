# 安装 mysql
```bash
brew install mysql
```
## 版本
```bash
mysql --version
# 启动
brew services start mysql or mysql.server start
```

### 首次登录
```bash
mysql -u root
```

### 如果提示 socket：
```bash
mysql -u root -p
``````

### 设置 root 密码
```bash
ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';
FLUSH PRIVILEGES;

exit;
```