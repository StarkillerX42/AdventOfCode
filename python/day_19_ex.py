def makeRules(fn):
  with open(fn) as file:
    raw = file.read().split("\n\n")
  rulesDict = {}
  for rule in raw[0].split("\n"):
    rule = rule.split(":")
    if "\"" in rule[1]:
      subrules = rule[1][2]
    elif "|" in rule[1]:
      subrules = [[int(j)for j in i.strip().split()] for i in rule[1].strip().split("|")]
    else:
      subrules = [int(i) for i in rule[1].strip().split(" ")]
    rulesDict[int(rule[0])] = subrules
  messages = raw[1].split("\n")

  return rulesDict, messages

def printRules(rulesDict):
  print("Printing Rules")
  for rule in rulesDict:
    print(str(rule) + ": " + str(rulesDict[rule]))
  print("Done.")

#Takes a formatted password string and calculates the length.
#Assumes all branches of the password are uniform in length.
#Input: "a[[aa|bb][ab|ba]|[ab|ba][aa|bb]]b"
#Output: 6
def getLen(rule): #Computes the length of password rules for isvalid.
  cur, count = 0, 0
  while cur < len(rule):
    if rule[cur] in ("a", "b"):
      count += 1
    elif rule[cur] == "|":
      depth = 1
      while depth > 0:
        cur += 1
        if rule[cur] == "|":
          depth += 1
        elif rule[cur] == "]":
          depth -= 1
    cur += 1

  return count

#Determines if a given message is valid against the formatted pasword string
#Inputs: (String) formatted password string, (String) message
#Output: Boolean 
def isValid(rule, message):
  ptrs = [0]
  mPtr = [0]
  ruleLen = getLen(rule)

  if len(message) != ruleLen:
    return False

  #Because we know that the length of the message matches the check exactly we know that once you get past the nth letter, you've passed.
  while ptrs:
    if mPtr[0] >= len(message):
      return True

    cur = rule[ptrs[0]] #Get the value pointed to by the current pointer
    if cur.isalpha(): #If it's a simple a or b, evaluate it. If it's bad, trash the pointers and start from the next one.
      if message[mPtr[0]] == cur:
        ptrs[0] += 1
        mPtr[0] += 1
      else:
        ptrs.pop(0)
        mPtr.pop(0)
    elif cur == "[": #Create a second pointer after the relevant "|". Watch for errant "["s. Increment pointer.
      tempPtr, depth = ptrs[0] + 1, 1
      while depth > 0:
        if rule[tempPtr] == "[":
          depth += 1
        elif rule[tempPtr] == "|":
          depth -= 1
        tempPtr += 1
      ptrs.append(tempPtr)
      mPtr.append(mPtr[0])
      ptrs[0] += 1
    elif cur == "|": # Skip forward to after the relevant "]". Watch for errant "["s.
      depth = 1
      while depth > 0:
        ptrs[0] += 1
        if rule[ptrs[0]] == "[":
          depth += 1
        elif rule[ptrs[0]] == "]":
          depth -= 1
      ptrs[0] += 1
    else: #Cur is at a "]", just increment it.
      ptrs[0] += 1

  #If you're run out of valid pointers to check, the rule must be invalid.
  return False

#Takes a set of rules and creates a formatter password string.
#Input: [4, 1, 5]
#Output: "a[[aa|bb][ab|ba]|[ab|ba][aa|bb]]b"
def getRule(ruleIdx):
  global rulesDict
  rule = rulesDict[ruleIdx]
  while not all(type(x) == str for x in rule):
    i = 0
    if type(rule[0]) == list:
        rule = ["["] + rule[0] + ["|"] + rule[1] + ["]"]

    while i < len(rule):
      instruction = rule[i]
      #print(str(i) + ": " + str(instruction))
      if type(instruction) == str:
        pass
      else:
        newInst = rulesDict[instruction]
        if type(newInst) == int or type(newInst) == str:
          rule = rule[:i] + [newInst] + rule[i + 1:]
        else:
          if type(newInst[0]) == int:
            rule = rule[:i] + newInst + rule[i + 1:]
          else:
            rule = rule[:i] + ["["] + newInst[0] + ["|"] + newInst[1] + ["]"] + rule[i + 1:]
      i += 1

  rule = "".join(rule)
  return rule

#Check message segments against rule 42 twice, then check it against 42 until it fails, then check it against 31 until it fails or you pass.
def part2():
  rule42, rule31 = getRule(42), getRule(31)
  ruleLen = getLen(rule42)
  count = 0

  for message in sorted(messages):
    if len(message) % ruleLen != 0 or len(message) < (ruleLen * 3):
      pass #Don't even bother validating.
    elif len(message) == (ruleLen * 3):
      if isValid(rule42 + rule42 + rule31, message):
        print(message)
      count += 1 if isValid(rule42 + rule42 + rule31, message) else 0
    else:
      if isValid(rule42, message[0:ruleLen]) and isValid(rule42, message[ruleLen:2*ruleLen]) and isValid(rule31, message[-ruleLen:]):
        midSegs = int(len(message) / ruleLen) - 3
        valid42 = all(isValid(rule42, message[(2+i)*ruleLen:(3+i)*ruleLen]) for i in range(int(midSegs/2) + midSegs%2))

        flag = 42
        for i in range(int(midSegs/2), 0, -1):
          if flag == 42: 
            flag = 42 if isValid(rule42, message[(i+1)*-ruleLen:i*-ruleLen]) else 31
          if flag == 31:
            flag = 31 if isValid(rule31, message[(i+1)*-ruleLen:i*-ruleLen]) else 0
        if flag > 0 and valid42:
            print(message)
        count += 1 if flag > 0 and valid42 else 0
      else:
        pass
  return count


rulesDict, messages = makeRules("dat/day_19.txt")
rule0 = getRule(0)
print(getLen(rule0))
#total = sum(isValid(rule0, message) for message in messages)
#print("Final count: " + str(total))

p2count = part2()
print("Final count: " + str(p2count))
