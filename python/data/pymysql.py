#!/bin/bash

import pymysql
import os

def quary(sql):
    '''定义数据库连接函数'''
    # 连接database
    conn = pymysql.connect(host="192.168.174.10", user="root", password="Password1", database="test", charset="utf8mb4")
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    # 定义要执行的SQL语句
    '''mysql 建表语句
    sql = """
    CREATE TABLE USER1 (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `user_id` bigint(20) DEFAULT NULL COMMENT '身份证号码',
    `auth_year` smallint(4) DEFAULT NULL COMMENT '认证年份',
    `auth_month` tinyint(4) DEFAULT NULL COMMENT '认证月份',
    `auth_image_url` varchar(256) DEFAULT NULL COMMENT '认证照片url',
    `is_confirm_result` char(1) DEFAULT NULL,
    `confirm_result_time` datetime DEFAULT NULL,
    `is_sync_result` char(1) DEFAULT NULL,
    `library_version` float DEFAULT NULL,
    `auth_category` varchar(64) DEFAULT NULL,
    `is_difficulty` char(1) DEFAULT NULL,
    `list_type` varchar(64) DEFAULT NULL,
    `check_status` varchar(10) DEFAULT NULL,
    `first_review_reason` varchar(64) DEFAULT NULL,
    `first_review_user_account` varchar(64) DEFAULT NULL,
    `first_review_user_name` varchar(64) DEFAULT NULL,
    `first_review_time` datetime DEFAULT NULL,
    `blocked_by` varchar(10) DEFAULT NULL,
    `check_result` varchar(64) DEFAULT NULL,
    `check_remark` varchar(64) DEFAULT NULL,
    `operate_user_name` varchar(64) DEFAULT NULL,
    `verify_user_name` varchar(64) DEFAULT NULL,
    `batch_import_remark` varchar(64) DEFAULT NULL,
    `is_living` varchar(10) DEFAULT NULL,
    `living_score` varchar(128) DEFAULT NULL,
    `server_auth_type` varchar(10) DEFAULT NULL,
    `caller` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`) USING BTREE,
    KEY `idx_agent_id_number` (`agent_user_id`) USING BTREE,
    KEY `idx_user_id` (`user_id`) USING BTREE,
    KEY `idx_auth_time` (`auth_time`) USING BTREE,
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    '''
    # 执行SQL语句
    cursor.execute(sql)
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()

def main(sql):
    sql = sql
    quary(sql)

if __name__ == "__main__":
    sql = """
        CREATE TABLE TEST (
        `id` bigint(20) NOT NULL AUTO_INCREMENT,
        `user_id` bigint(20) DEFAULT NULL COMMENT '身份证号码',
        `auth_year` smallint(4) DEFAULT NULL COMMENT '认证年份',
        `auth_month` tinyint(4) DEFAULT NULL COMMENT '认证月份',
        `auth_image_url` varchar(256) DEFAULT NULL COMMENT '认证照片url',
        `is_confirm_result` char(1) DEFAULT NULL,
        `confirm_result_time` datetime DEFAULT NULL,
        `is_sync_result` char(1) DEFAULT NULL,
        `library_version` float DEFAULT NULL,
        `auth_category` varchar(64) DEFAULT NULL,
        `is_difficulty` char(1) DEFAULT NULL,
        `list_type` varchar(64) DEFAULT NULL,
        `check_status` varchar(10) DEFAULT NULL,
        `first_review_reason` varchar(64) DEFAULT NULL,
        `first_review_user_account` varchar(64) DEFAULT NULL,
        `first_review_user_name` varchar(64) DEFAULT NULL,
        `first_review_time` datetime DEFAULT NULL,
        `blocked_by` varchar(10) DEFAULT NULL,
        `check_result` varchar(64) DEFAULT NULL,
        `check_remark` varchar(64) DEFAULT NULL,
        `operate_user_name` varchar(64) DEFAULT NULL,
        `verify_user_name` varchar(64) DEFAULT NULL,
        `batch_import_remark` varchar(64) DEFAULT NULL,
        `is_living` varchar(10) DEFAULT NULL,
        `living_score` varchar(128) DEFAULT NULL,
        `server_auth_type` varchar(10) DEFAULT NULL,
        `caller` varchar(255) DEFAULT NULL,
        PRIMARY KEY (`id`) USING BTREE,
        KEY `idx_user_id` (`user_id`) USING BTREE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
    main(sql)