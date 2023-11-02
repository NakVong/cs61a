passphrase = 'slinky'

def midsem_survey(p):
    """
    You do not need to understand this code.
    >>> midsem_survey(passphrase)
    '083405e24afb7fe627c935f5c078cd7273590b80c691569b86d6bc03'
    """
    import hashlib
    return hashlib.sha224(p.encode('utf-8')).hexdigest()


class VendingMachine:
    """A vending machine that vends some product for some price.

    >>> v = VendingMachine('candy', 10)
    >>> v.vend()
    'Nothing left to vend. Please restock.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'
    >>> v.restock(2)
    'Current candy stock: 2'
    >>> v.vend()
    'Please add $10 more funds.'
    >>> v.add_funds(7)
    'Current balance: $7'
    >>> v.vend()
    'Please add $3 more funds.'
    >>> v.add_funds(5)
    'Current balance: $12'
    >>> v.vend()
    'Here is your candy and $2 change.'
    >>> v.add_funds(10)
    'Current balance: $10'
    >>> v.vend()
    'Here is your candy.'
    >>> v.add_funds(15)
    'Nothing left to vend. Please restock. Here is your $15.'

    >>> w = VendingMachine('soda', 2)
    >>> w.restock(3)
    'Current soda stock: 3'
    >>> w.restock(3)
    'Current soda stock: 6'
    >>> w.add_funds(2)
    'Current balance: $2'
    >>> w.vend()
    'Here is your soda.'
    """
    "*** YOUR CODE HERE ***"
    def __init__(self, item, price):
        assert price > 0
        self.item = item
        self.price = price
        self.num_item = 0
        self.balance = 0

    def restock(self, num_item):
        assert num_item > 0
        self.num_item += num_item
        print(f"'Current {self.item} stock: {self.num_item}'")

    def add_funds(self, funds):
        assert funds > 0
        if self.num_item == 0:
            print(f"'Nothing left to vend. Please restock. Here is your ${funds}.'")
        else:
            self.balance += funds
            print(f"'Current balance: ${self.balance}'")

    def vend(self):
        if self.num_item > 0 and self.balance == self.price:
            print(f"'Here is your {self.item}.'")
            self.num_item -= 1
            self.balance = 0
        elif self.num_item > 0 and self.balance > self.price:
            print(f"'Here is your {self.item} and ${self.balance - self.price} change.'")
            self.num_item -= 1
            self.balance = 0
        elif self.num_item > 0 and self.balance < self.price:
            print(f"'Please add ${self.price - self.balance} more funds.'")
        elif self.num_item == 0 and self.balance > self.price:
            print(f"'Nothing left to vend. Please restock. Here is your ${self.balance}.'")
        elif self.num_item == 0 and self.balance == 0:
            print(f"'Nothing left to vend. Please restock.'")


def store_digits(n):
    """Stores the digits of a positive number n in a linked list.

    >>> s = store_digits(1)
    >>> s
    Link(1)
    >>> store_digits(2345)
    Link(2, Link(3, Link(4, Link(5))))
    >>> store_digits(876)
    Link(8, Link(7, Link(6)))
    >>> store_digits(2450)
    Link(2, Link(4, Link(5, Link(0))))
    >>> # a check for restricted functions
    >>> import inspect, re
    >>> cleaned = re.sub(r"#.*\\n", '', re.sub(r'"{3}[\s\S]*?"{3}', '', inspect.getsource(store_digits)))
    >>> print("Do not use str or reversed!") if any([r in cleaned for r in ["str", "reversed"]]) else None
    """
    "*** YOUR CODE HERE ***"
    if n // 10 == 0:
        return Link(n)
    else:
        get_digit = n
        counter = 0
        while get_digit > 10:
            get_digit //= 10
            counter += 1
        return Link(get_digit, store_digits(n - get_digit * 10 ** counter))


def deep_map_mut(func, lnk):
    """Mutates a deep link lnk by replacing each item found with the
    result of calling func on the item. Does NOT create new Links (so
    no use of Link's constructor).

    Does not return the modified Link object.

    >>> link1 = Link(3, Link(Link(4), Link(5, Link(6))))
    >>> print(link1)
    <3 <4> 5 6>
    >>> # Disallow the use of making new Links before calling deep_map_mut
    >>> Link.__init__, hold = lambda *args: print("Do not create any new Links."), Link.__init__
    >>> try:
    ...     deep_map_mut(lambda x: x * x, link1)
    ... finally:
    ...     Link.__init__ = hold
    >>> print(link1)
    <9 <16> 25 36>
    """
    "*** YOUR CODE HERE ***"
    if isinstance(lnk.first, Link):
        deep_map_mut(func, lnk.first)
    else:
        lnk.first = func(lnk.first)
        
    if lnk.rest != Link.empty:
        deep_map_mut(func, lnk.rest)


def two_list(vals, counts):
    """
    Returns a linked list according to the two lists that were passed in. Assume
    vals and counts are the same size. Elements in vals represent the value, and the
    corresponding element in counts represents the number of this value desired in the
    final linked list. Assume all elements in counts are greater than 0. Assume both
    lists have at least one element.
    >>> a = [1, 3]
    >>> b = [1, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(3))
    >>> a = [1, 3, 2]
    >>> b = [2, 2, 1]
    >>> c = two_list(a, b)
    >>> c
    Link(1, Link(1, Link(3, Link(3, Link(2)))))
    """
    "*** YOUR CODE HERE ***"
    lst = Link(vals[0])
    current = lst
    while counts[0] > 1:
        current.rest = Link(vals[0])
        current = current.rest
        counts[0] -= 1

    for i in range(1, len(vals)):
        while counts[i] > 0:
            current.rest = Link(vals[i])
            current = current.rest
            counts[i] -= 1

    return lst


class Link:
    """A linked list.

    >>> s = Link(1)
    >>> s.first
    1
    >>> s.rest is Link.empty
    True
    >>> s = Link(2, Link(3, Link(4)))
    >>> s.first = 5
    >>> s.rest.first = 6
    >>> s.rest.rest = Link.empty
    >>> s                                    # Displays the contents of repr(s)
    Link(5, Link(6))
    >>> s.rest = Link(7, Link(Link(8, Link(9))))
    >>> s
    Link(5, Link(7, Link(Link(8, Link(9)))))
    >>> print(s)                             # Prints str(s)
    <5 7 <8 9>>
    """
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'

