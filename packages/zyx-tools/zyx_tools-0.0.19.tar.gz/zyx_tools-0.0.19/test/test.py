import sys

sys.path.append("../../tools")
from zyx_tools import SvnTool, OtherTool


def Test_svn_exteral():
    res = SvnTool.get_svn_externals(
        "svn://192.168.0.12/flower/trunk/server/script/",
        "",
        "",
    )
    print("\r\n".join(res))


def test_svn_getlog():
    res = SvnTool.get_svn_log(
        "svn://192.168.0.12/flower/trunk/client/WholeClient",
        "2023-09-26",
        "2023-09-28",
        search="合并",
    )
    for item in res:
        print(item.json(exclude_none=True, ensure_ascii=False))


def test_svn_ls():
    try:
        res = SvnTool.get_svn_ls("svn://192.168.0.12/flower/trunk/client/WholeClient1")
        for item in res:
            print(item)
    except Exception as e:
        print(f"err:{e}")


if __name__ == "__main__":
    OtherTool.init_log()
    # Test_svn_exteral()
    # test_svn_getlog()
    test_svn_ls()
