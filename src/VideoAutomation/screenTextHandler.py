from . import VideoConstants as vc
import cv2


class StringManipulator:
    def calculateSpaces(self, k, c, temp):
        totalspace = k - c
        singlespace = totalspace // (len(temp) - 1)
        spacelist = [' ' * int(singlespace)] * (len(temp) - 1)
        totalspacetillnow = singlespace * (len(temp) - 1)
        tt = totalspace - totalspacetillnow
        # print(spacelist, temp)
        i = 0
        while (tt):
            spacelist[i] = spacelist[i] + ' '
            i += 1
            tt -= 1
        tempans = ""
        for j in range(len(temp) - 1):
            tempans += temp[j] + spacelist[j]
        tempans += temp[-1]
        return tempans

    def wrap_in_lines(self, lines, k):
        st = ' '.join(lines)

        ans = []
        c = 0
        temp = []
        for word in list(st.split()):
            if c + len(temp) + len(word) > k:
                tempans = temp[-1]
                if len(temp) > 1:
                    tempans = self.calculateSpaces(k, c, temp)
                ans.append(tempans)
                temp = [word]
                # print(ans)
                c = len(word)
            else:
                temp.append(word)
                c += len(word)

        if len(temp) == 1:
            ans.append(temp[-1])
            return ans
        if len(temp) == 0:
            return ['']
        tempans = self.calculateSpaces(k, c, temp)
        tempans = ' '.join(tempans.split())
        ans.append(tempans)

        return ans


def set_screen_text(frame, screenft, data):
    wrap = StringManipulator()
    lines = wrap.wrap_in_lines([data], vc.TEXT_CHAR_WRAP)
    text_x = vc.TEXT_POS_X
    text_y = vc.TEXT_POS_Y
    increase_y = 0
    mainlines = []
    for text in lines:
        text = text.strip().split('.')
        text = '. '.join(text)
        mainlines.append(text)
    for text in mainlines:
        screenft.putText(frame, text, (text_x, text_y+increase_y), vc.TEXT_CHAR_SIZE, vc.TEXT_COLOR, -1, cv2.LINE_AA, True)
        increase_y += vc.TEXT_HORIZONTAL_SEPARATE
    return frame
