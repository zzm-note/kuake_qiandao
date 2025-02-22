from datetime import datetime
from pprint import pprint
from loguru import logger
import httpx
import os

kps = os.getenv("QUARK_KPS")
sign = os.getenv("QUARK_SIGN")
vcode = os.getenv("QUARK_VCODE")

if kps is None or sign is None or vcode is None:
    logger.error("请设置 QUARK_KPS")
    raise ValueError("请设置 QUARK_KPS")


def query_balance():
    """
    查询抽奖余额
    """
    url = "https://coral2.quark.cn/currency/v1/queryBalance"
    querystring = {
        "moduleCode": "1f3563d38896438db994f118d4ff53cb",
        "kps": kps,
    }
    response = httpx.get(url=url, params=querystring)
    response.raise_for_status()
    pprint(response.json())


def human_unit(bytes_: int) -> str:
    """
    人类可读单位
    :param bytes_: 字节数
    :return: 返回 MB GB TB
    """
    units = ("MB", "GB", "TB", "PB")
    bytes_ = bytes_ / 1024 / 1024
    i = 0
    while bytes_ >= 1024:
        bytes_ /= 1024
        i += 1
    return f"{bytes_:.2f} {units[i]}"


def user_info():
    """
    获取用户信息
    :return: None
    """
    url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
    querystring = {
        "pr": "ucpro",
        "fr": "android",
        "kps": kps,
        "sign": sign,
        "vcode": vcode,
    }
    response = httpx.get(url=url, params=querystring)
    response.raise_for_status()
    content = response.json()
    if content["code"] != 0:
        logger.warning(content["message"])
    else:
        data = content["data"]
        super_vip_exp_at = datetime.fromtimestamp(
            data["super_vip_exp_at"] / 1000
        ).strftime("%Y-%m-%d %H:%M:%S")
        logger.info(
            f"会员类型：{data['member_type']}, 过期时间：{super_vip_exp_at}, 总计容量：{human_unit(data['total_capacity'])}"
            f", 使用容量：{human_unit(data['use_capacity'])}, 使用百分比：{data['use_capacity'] / data['total_capacity'] * 100:.2f}%"
        )
        cap_sign = data["cap_sign"]
        if cap_sign["sign_daily"]:
            logger.success(
                f"已签到成功，获得容量: {human_unit(cap_sign['sign_daily_reward'])}, 签到进度: {cap_sign['sign_progress']}"
            )


def checkin():
    """
    签到
    :return: None
    """
    url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
    querystring = {
        "pr": "ucpro",
        "fr": "android",
        "kps": kps,
        "sign": sign,
        "vcode": vcode,
    }
    response = httpx.post(url=url, json={"sign_cyclic": True}, params=querystring)
    if response.status_code == 200:
        if response.json()["code"] != 0:
            logger.warning(response.json()["message"])
        else:
            logger.success(
                f"签到成功，获得容量: {human_unit(response.json()['data']['sign_daily_reward'])}"
            )
    else:
        logger.warning(f"签到失败，状态码: {response.status_code}")


if __name__ == "__main__":
    # query_balance()
    checkin()
    # user_info()
