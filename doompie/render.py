import pygame

from doompie import WADMap


def make_lines(
    map: 'WADMap',
):
    vertices = tuple(
        (vertex.x, vertex.y)
        for vertex in map.vertexes
    )
    edges = tuple(
        (linedef.beginning_vertex, linedef.ending_vertex)
        for linedef in map.linedefs
    )
    return vertices, edges


def render(
    map: WADMap,
) -> None:
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    done = False
    is_blue = True
    x = 0
    y = 0

    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP] or pressed[pygame.K_w]:
            y -= 3
        if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
            y += 3
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            x -= 3
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            x += 3
        if pressed[pygame.K_ESCAPE]:
            done = True

        screen.fill(color=(127, 127, 127))
        for linedef in map.linedefs:
            start_pos = map.vertexes[linedef.beginning_vertex]
            end_pos = map.vertexes[linedef.ending_vertex]
            pygame.draw.line(
                screen,
                color=(0, 0, 0),
                start_pos=(x - start_pos.x//3 + 400, y - start_pos.y//3 + 500),
                end_pos=(x - end_pos.x//3 + 400, y - end_pos.y//3 + 500),
                width=2,
            )
        pygame.display.flip()
        clock.tick(60)
