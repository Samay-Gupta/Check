from Additional.Encryption import Encryption
from currency_converter import CurrencyConverter
import os


class UserData:
    def __init__(self, drt="Additional", filename="User_Data_Encrypted.txt", rt="Routes.txt"):
        if drt != "":
            filename = drt + "\\" + filename
            rt = drt + "\\" + rt
        self.file = os.getcwd() + "\\" + filename
        with open(rt, 'r') as route_list:
            self.route_data = eval(route_list.read())
        self.encryption_manager = Encryption()
        self.country_id = "SWE"
        self.converter = CurrencyConverter()
        self.id_size = 8
        self.base_cost = 1
        self.main_cur = "USD"
        self.pref_cur = "SEK"

    def conv(self, amt=0):
        return self.converter.convert(amt, self.main_cur, self.pref_cur)

    def add(self, name, number="", mail=""):
        if number == "" and mail == "":
            result = (0, "Phone Number/ Email required to set-up card", None)
        else:
            with open(self.file, 'r') as editor:
                data = eval(self.encryption_manager.decrypt(editor.read()))
            num = len(data.keys())
            id_code = self.country_id + "0"*(self.id_size-num) + str(num)
            data[id_code] = {}
            data[id_code]["balance"] = 0
            data[id_code]["start_loc"] = ""
            data[id_code]["end_loc"] = ""
            data[id_code]["name"] = name
            data[id_code]["phone"] = number
            data[id_code]["email"] = mail
            data[id_code]["stops"] = 0
            data[id_code]["active"] = False
            data[id_code]["route_no"] = ""
            data[id_code]["history"] = []
            self.save(data)
            result = (1, "User Added, ID:{}".format(id_code), id_code)
        print(result[1])
        return result

    def load(self, id_code="", amt=0):
        cost = amt*self.base_cost
        if self.pref_cur != self.main_cur:
            cost = self.conv(cost)
        print("Cost is {} {} ".format(cost, self.pref_cur))
        if id_code == "":
            result = (0, "Valid ID required", None)
        else:
            with open(self.file, 'r') as editor:
                data = eval(self.encryption_manager.decrypt(editor.read()))
            if id_code not in data.keys():
                result = (0, "Invalid card", None)
            else:
                data[id_code]["balance"] += amt
                self.save(data)
                result = (1, "Card {} is loaded with {} Balance available is {}".format(id_code, amt, data[id_code]["balance"]), data[id_code]["balance"])

        print(result[1])
        return result

    def check(self, id_code):
        with open(self.file, 'r') as editor:
            data = eval(self.encryption_manager.decrypt(editor.read()))
        print(data.keys())
        if id_code not in data.keys():
            return False
        else:
            return True

    def enable(self, id_code=""):
        if id_code == "":
            result = (0, "Valid ID required", None)
        else:
            with open(self.file, 'r') as editor:
                data = eval(self.encryption_manager.decrypt(editor.read()))
            if id_code not in data.keys():
                result = (0, "Invalid card", None)
            else:
                data[id_code]["active"] = True
                self.save(data)
                result = (1, "Card {} Activated".format(id_code), id_code)
        print(result[1])
        return result

    def disable(self, id_code=""):
        if id_code == "":
            result = (0, "Valid ID required", None)
        else:
            with open(self.file, 'r') as editor:
                data = eval(self.encryption_manager.decrypt(editor.read()))
            if id_code not in data.keys():
                result = (0, "Invalid card", None)
            else:
                data[id_code]["active"] = False
                self.save(data)
                result = (1, "Card {} Deactivated".format(id_code), id_code)
        print(result[1])
        return result

    def cost(self, frm="", to="", route=""):
        stop_names = [i for (i,j) in self.route_data[route]]
        frm_ind = stop_names.index(frm)
        to_ind = stop_names.index(to)
        dist = eval(self.route_data[route][to_ind][1]) - eval(self.route_data[route][frm_ind][1])
        if dist <= 0.5:
            cost = 5
        else:
            cost = 5 + (dist-0.5)+self.base_cost
        return cost

    def calc(self, id_code="", loc="", route=""):
        if id_code == "":
            result = (0, "Valid ID required", None)
        else:
            with open(self.file, 'r') as editor:
                data = eval(self.encryption_manager.decrypt(editor.read()))
            if id_code not in data.keys():
                result = (0, "Invalid card", None)
            else:
                if data[id_code]["active"]:
                    if data[id_code]["start_loc"] == "":
                        if data[id_code]["balance"] > 0.5:
                            data[id_code]["start_loc"] = loc
                            data[id_code]["route_no"] = route
                            result = (1, "Boarded at {}. Bus {}".format(loc, route), loc)
                            self.save(data)
                        else:
                            result = (0, "Insufficient Balance. Reload Card", None)
                    else:
                        data[id_code]["stop_loc"] = loc
                        fare = self.cost(data[id_code]["start_loc"], data[id_code]["stop_loc"], data[id_code]["route_no"])
                        data[id_code]["balance"] -= fare
                        summary = (data[id_code]["start_loc"], data[id_code]["stop_loc"], data[id_code]["route_no"], fare)
                        data[id_code]["history"].append(summary)
                        data[id_code]["start_loc"] = ""
                        data[id_code]["stop_loc"] = ""
                        data[id_code]["route_no"] = ""
                        result = (2, "Transaction successful cost is {}. Balance remaining is {}".format(fare, data[id_code]["balance"]))
                        self.save(data)
                else:
                    result = (0, "Card is inactive. Activate it and try again.", None)
        print(result[1])
        return result

    def save(self, data=""):
        with open(self.file, 'w') as editor:
            editor.write(self.encryption_manager.encrypt(str(data)))

