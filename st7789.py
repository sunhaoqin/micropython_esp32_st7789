from rgb import DisplaySPI, color565
import ustruct


_NOP = const(0x00)
_SWRESET = const(0x01)
_RDDID = const(0x04)
_RDDST = const(0x09)

_SLPIN = const(0x10)
_SLPOUT = const(0x11)
_PTLON = const(0x12)
_NORON = const(0x13)

_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_RAMRD = const(0x2E)

_PTLAR = const(0x30)
_COLMOD = const(0x3A)
_MADCTL = const(0x36)

_FRMCTR1 = const(0xB1)
_FRMCTR2 = const(0xB2)
_FRMCTR3 = const(0xB3)
_INVCTR = const(0xB4)
_DISSET5 = const(0xB6)

_PWCTR1 = const(0xC0)
_PWCTR2 = const(0xC1)
_PWCTR3 = const(0xC2)
_PWCTR4 = const(0xC3)
_PWCTR5 = const(0xC4)
_VMCTR1 = const(0xC5)

_RDID1 = const(0xDA)
_RDID2 = const(0xDB)
_RDID3 = const(0xDC)
_RDID4 = const(0xDD)

_PWCTR6 = const(0xFC)

_GMCTRP1 = const(0xE0)
_GMCTRN1 = const(0xE1)


class ST7789(DisplaySPI):
    """
    A simple driver for the ST7789-based displays.
    >>> from machine import Pin, SPI
    >>> import st7789
    >>> display = st7789.ST7789(SPI(1), dc=Pin(12), cs=Pin(15), rst=Pin(16))
    >>> display = st7789.ST7789R(SPI(1, baudrate=40000000), dc=Pin(12), cs=Pin(15), rst=Pin(16))
    >>> display.fill(0x7521)
    >>> display.pixel(64, 64, 0)
    """
    _COLUMN_SET = _CASET
    _PAGE_SET = _RASET
    _RAM_WRITE = _RAMWR
    _RAM_READ = _RAMRD
    _INIT = (
        (_SWRESET, None),
        (_SLPOUT, None),
        (_COLMOD, b"\x55"),  # 16bit color
        (_MADCTL, b"\x08"),
    )

    def __init__(self, spi, dc, cs, rst=None, width=240, height=240):
        super().__init__(spi, dc, cs, rst, width, height)

    def init(self):

        super().init()
        cols = ustruct.pack(">HH", 0, self.width)
        rows = ustruct.pack(">HH", 0, self.height)
        for command, data in (
            (_CASET, cols),
            (_RASET, rows),
            (_INVON, None),
            (_NORON, None),
            (_DISPON, None),
            (_MADCTL, b"\xc0"),  # Set rotation to 0 and use RGB
        ):
            self._write(command, data)
