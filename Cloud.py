'''class Cloud (self,game):
        super(cloud, self).__init__()  # Initialise la classe parente Sprite
        self.game = game
        # Load the image
        self.original_image = py.image.load("cloud.png").convert_alpha()
        # Resize at 80x80 pixels
        self.image = py.transform.scale(self.original_image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = x_init  # Position initiale x
        self.rect.y = y_init  # Position initiale y'''
        
