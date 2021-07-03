#!/usr/bin/env python

import configparser
import os
import pymysql


class Backend:
    backendId = ''
    cluster = ''
    ip = ''
    heartbeatPort = ''
    bePort = ''
    httpPort = ''
    brpcPort = ''
    lastStartTime = ''
    lastHeartbeatTime = ''
    alive = ''
    systemDecommissioned = ''
    clusterDecommissioned = ''
    tabletNum = ''
    dataUsedCapacity = ''
    availCapacity = ''
    totalCapacity = ''
    usedPct = ''
    maxDiskUsedPct = ''
    errMesg = ''
    version = ''
    status = ''


class Backends:
    url = ''
    connect_db = ''
    bes = []

    def __init__(self):
        self.connect_db = 'information_schema'

    def getData(self):
        db = pymysql.connect(
            host=fe_ip,
            port=int(fe_port),
            user=dorisdb_user,
            password=dorisdb_password,
            db=self.connect_db)

        cursor = db.cursor()

        cursor.execute("show backends")

        results = cursor.fetchall()
        for row in results:
            dorisdb_be = Backend()
            dorisdb_be.backendId = row[0]
            dorisdb_be.cluster = row[1]
            dorisdb_be.ip = row[2]
            dorisdb_be.heartbeatPort = row[3]
            dorisdb_be.bePort = row[4]
            dorisdb_be.httpPort = row[5]
            dorisdb_be.brpcPort = row[6]
            dorisdb_be.lastStartTime = row[7]
            dorisdb_be.lastHeartbeatTime = row[8]
            dorisdb_be.alive = row[9]
            dorisdb_be.systemDecommissioned = row[10]
            dorisdb_be.clusterDecommissioned = row[11]
            dorisdb_be.tabletNum = row[12]
            dorisdb_be.dataUsedCapacity = row[13]
            dorisdb_be.availCapacity = row[14]
            dorisdb_be.totalCapacity = row[15]
            dorisdb_be.usedPct = row[16]
            dorisdb_be.maxDiskUsedPct = row[17]
            dorisdb_be.errMesg = row[18]
            dorisdb_be.version = row[19]
            dorisdb_be.status = row[20]
            self.bes.append(dorisdb_be)

        db.close()
        return self.bes


class MemTracker:
    url = ''
    output_file = ''

    def __init__(self, dorisdb_be):
        self.url = dorisdb_be.ip + ":" + dorisdb_be.httpPort + "/mem_tracker"
        self.output_file = output_dir + "/" + str(dorisdb_be.backendId) + "/mem_tracker.html"

    def getData(self):
        res = os.popen('curl %s' % self.url).readlines()

        f = open(self.output_file, 'w')
        for item in res:
            f.write(item)
        f.close()


class MemZ:
    url = ''
    output_file = ''

    def __init__(self, dorisdb_be):
        self.url = dorisdb_be.ip + ":" + dorisdb_be.httpPort + "/memz"
        self.output_file = output_dir + "/" + str(dorisdb_be.backendId) + "/memz.html"

    def getData(self):
        res = os.popen('curl %s' % self.url).readlines()

        f = open(self.output_file, 'w')
        for item in res:
            f.write(item)
        f.close()


class Growth:
    url = ''
    bin_file = "./bin/pprof"
    output_file = ''

    def __init__(self, dorisdb_be):
        self.url = 'http://' + dorisdb_be.ip + ":" + dorisdb_be.httpPort + '/pprof/growth'
        self.output_file = output_dir + "/" + str(dorisdb_be.backendId) + "/growth.dot"

    def getData(self):
        os.system(self.bin_file + " --dot " + self.url + " > " + self.output_file)


class Metrics:
    url = ''
    output_file = ''

    def __init__(self, dorisdb_be):
        self.url = 'http://' + dorisdb_be.ip + ":" + dorisdb_be.httpPort + "/metrics"
        self.output_file = output_dir + "/" + str(dorisdb_be.backendId) + "/metrics.txt"

    def getData(self):
        res = os.popen('curl %s' % self.url).readlines()

        f = open(self.output_file, 'w')
        for item in res:
            f.write(item)
        f.close()


class Machine:
    url = ''
    output_file = ''

    def __init__(self, dorisdb_be):
        self.url = 'http://' + dorisdb_be.ip + ":" + dorisdb_be.httpPort
        self.output_file = output_dir + "/" + str(dorisdb_be.backendId) + "/machine.html"

    def getData(self):
        res = os.popen('curl %s' % self.url).readlines()

        f = open(self.output_file, 'w')
        for item in res:
            f.write(item)
        f.close()


class Varz:
    url = ''
    output_file = ''

    def __init__(self, dorisdb_be):
        self.url = 'http://' + dorisdb_be.ip + ":" + dorisdb_be.httpPort + "/varz"
        self.output_file = output_dir + "/" + str(dorisdb_be.backendId) + "/varz.html"

    def getData(self):
        res = os.popen("curl %s" % self.url).readlines()

        f = open(self.output_file, 'w')
        for item in res:
            f.write(item)
        f.close()


if __name__ == "__main__":
    file = "config.ini"
    conf = configparser.ConfigParser()
    conf.read(file, encoding='utf-8')
    sections = conf.sections()
    commonConf = conf.items('common')
    commonConf = dict(commonConf)

    fe_ip = commonConf.get("fe_ip")
    fe_port = commonConf.get("fe_port")
    dorisdb_user = commonConf.get("user")
    dorisdb_password = commonConf.get("password")
    output_dir = "./output"

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    backends = Backends()
    bes = backends.getData()

    for be in bes:
        be_path = "./" + output_dir + "/" + str(be.backendId)
        if not os.path.exists(be_path):
            os.mkdir(output_dir + "/" + str(be.backendId))

        # 获取 MemTracker
        mem_tracker = MemTracker(be)
        mem_tracker.getData()

        # 获取 MemZ
        mem_z = MemZ(be)
        mem_z.getData()

        # 获取 Growth
        # dot -Tps filename.dot -o outfile.ps
        growth = Growth(be)
        growth.getData()

        # 获取 Metrics
        metrics = Metrics(be)
        metrics.getData()

        # 获取机器信息
        machine = Machine(be)
        machine.getData()

        # 获取 BE 配置
        varz = Varz(be)
        varz.getData()
