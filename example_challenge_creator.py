from twizzle import Twizzle


if __name__ == "__main__":
    sDBPath = "test.db"
    tw = Twizzle(sDBPath)

    sChallengeName = "image_hashing_challenge_print_scan_1"

    aOriginals = ["_img/p1.png", "_img/p2.png", "_img/p3.png", "_img/p1.png",
                  "_img/p1.png", "_img/p2.png", "_img/p2.png", "_img/p3.png", "_img/p3.png"]
    aComparatives = ["_img/p1_S.png", "_img/p3.png",
                     "_img/p3_S.png", "_img/p2.png", "_img/p3.png", "_img/p1.png", "_img/p3.png", "_img/p1.png", "_img/p2.png"]
    aTargetDecisions = [True, False, True,
                        False, False, False, False, False, False]

    dicMetadata = {
        "printer": "DC783",
        "paper": "recycled paper",
        "print_dpi": 300
    }

    tw.add_challenge(sChallengeName, aOriginals,
                     aComparatives, aTargetDecisions, dicMetadata)
