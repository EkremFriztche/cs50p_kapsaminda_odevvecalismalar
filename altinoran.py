import turtle #gemini hazırladı çöp çöp çöp
t = turtle.Turtle()
t.speed(0)
t.color("yellow")
t.pensize(2)

def draw_infinite_spiral_with_zoom():
  screen = turtle.Screen()
  screen.bgcolor("black")
  screen.setup(800, 800)  # Pencere boyutu

  # Başlangıç Fibonacci değerleri
  a = 0
  b = 1

  # Kamera sınırları (Başlangıçta dar bir alana odaklanır)
  view_size = 50

  print(
      "Otomatik uzaklaştırmalı sarmal çiziliyor... Durdurmak için kapatın."
  )

  while True:
    # Kamera sınırlarını sarmal büyüdükçe dinamik olarak genişlet (Zoom Out)
    # Parametreler: (sol_x, alt_y, sağ_x, üst_y)
    screen.setworldcoordinates(
        -view_size, -view_size, view_size * 1.5, view_size * 1.5
    )

    # 90 derecelik çeyrek çember çiz
    t.circle(b, 90)

    # Bir sonraki Fibonacci sayısını hesapla
    a, b = b, a + b

    # Sarmal büyüdükçe görüş alanını da katlayarak büyüt
    view_size += b


if __name__ == "__main__":
  draw_infinite_spiral_with_zoom()
