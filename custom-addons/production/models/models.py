from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    plante_id = fields.Many2one('gestion_culture.plante', string='Plante')
    vache_id = fields.Many2one('reproduction.vache', string='Vache')
    quantite_lait = fields.Float('Quantité (L)', help='Quantité en litres')
    date = fields.Date(string='Date de production', required=True, tracking=True)
    type_lait = fields.Selection([('vache', 'Lait de vache')], string='Type de lait')
    teneur_mat_grasse = fields.Float('Teneur en matière grasse (%)')
    teneur_proteine = fields.Float('Teneur en protéines (%)')
    technicien_id = fields.Many2one('hr.employee', string='Technicien')
    prix_vente = fields.Float('Prix de vente', compute='_compute_prix_vente', store=True) 
    quantite = fields.Float('Quantité (Kilos)', help='Quantité en kilos')
    longueur = fields.Float(string='Longueur')
    responsable_id = fields.Many2one('hr.employee', string='Responsable')
    statut = fields.Selection([('en_cours', 'En cours'), ('recolte', 'Récolté')], string='Statut')

    @api.depends('quantite')
    def _compute_prix_vente(self):
        for product in self:
            product.prix_vente = product.quantite * 1

class PlanificationProduction(models.Model):
    _name = 'production.planning'
    _description = "Planification de la production"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    reference = fields.Char(string="Reference", required=True, copy=False, readonly=True, default=lambda self: _('New'))    
    date_planifiee = fields.Date('Date planifiée', required=True)
    vache_id = fields.Many2one('reproduction.vache', string='Vache')
    plante_id = fields.Many2one('gestion_culture.plante', string='Plante')
    note = fields.Text('Note')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')], string='Status', default='draft', tracking=True)

    def action_confirm(self):
        self.status = 'confirm'

class NiveauStock(models.Model):
    _name = 'production.level'
    _description = 'Niveaux de stock'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    produit_reference = fields.Many2one('product.template', string='Produit', required=True)
    quantite_en_stock_lait = fields.Float('Quantité en stock Lait', compute='_compute_quantite_en_stock_lait', store=True)
    quantite_stock_kg = fields.Float('Quantité en stock', compute='_compute_quantite_stock_kg', store=True)
    type_lait = fields.Selection([('vache', 'Lait de vache')], string='Type de lait')
    vache_id = fields.Many2one('reproduction.vache', string='Vache')
    date = fields.Date('Date')
    note = fields.Text('Note')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')], string='Status', default='draft', tracking=True)

    @api.depends('produit_reference', 'produit_reference.quantite_lait')
    def _compute_quantite_en_stock_lait(self):
        for record in self:
            total_quantity = sum(record.mapped('produit_reference.quantite_lait'))
            record.quantite_en_stock_lait = total_quantity

    @api.depends('produit_reference', 'produit_reference.quantite')
    def _compute_quantite_stock_kg(self):
        for record in self:
            total_quantity = sum(record.mapped('produit_reference.quantite'))
            record.quantite_stock_kg = total_quantity

    def action_confirm(self):
        self.status = 'confirm'

class Stock(models.Model):
    _name = 'production.niveau'
    _description = 'Niveaux stock'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    produit_reference = fields.Many2one('product.template', string='Produit', required=True)
    quantite_stock_kg = fields.Float('Quantité en stock', compute='_compute_quantite_stock_kg', store=True)
    plante_id = fields.Many2one('gestion_culture.plante', string='Plante')
    date = fields.Date('Date')
    note = fields.Text('Note')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')], string='Status', default='draft', tracking=True)

    @api.depends('produit_reference', 'produit_reference.quantite')
    def _compute_quantite_stock_kg(self):
        for record in self:
            record.quantite_stock_kg = record.produit_reference.quantite 

    def action_confirm(self):
        self.status = 'confirm'


   
class StockMove(models.Model):
    _name = 'production.mvt'
    _description = 'Niveaux de stock'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    type_lait = fields.Selection([('vache', 'Lait de vache'), ], string='Type de lait', required=True)

    quantite_en_stock_lait = fields.Float(string='Quantité en stock (litre)', compute='_compute_quantite_en_stock_lait', store=True)
    quantite_saisie = fields.Float(string='Quantité saisie (litre)', required=True)
    date_mouvement = fields.Date(string="Date de mouvement", default=fields.Date.today)
    type_mouvement = fields.Selection([
    ('livraison', 'Livraison'),
    ('importation', 'Importation'),
    ('transfert', 'Transfert')], 
    string='Type de mouvement', required=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')], string='Status', default='draft', tracking=True)
    message_follower_ids = fields.One2many('mail.followers', 'res_id', string="Suiveurs")
    activity_ids = fields.One2many('mail.activity', 'res_id', string="Activités")
    message_ids = fields.One2many('mail.message', 'res_id', string="Messages")
    methode_paiement = fields.Selection([
    ('espece', 'Espèces'),
    ('carte', 'Carte de crédit'),
    ('virement', 'Virement bancaire'),
    ('cheque', 'Chèque')], 
    string='Méthode de paiement')
    prix = fields.Float(string='Prix', compute='_compute_prix', store=True)
   
    @api.constrains('quantite_saisie')
    def _check_quantite_disponible(self):
        for record in self:
            if record.quantite_saisie > record.quantite_en_stock_lait:
                raise UserError("La quantité saisie n'est pas disponible en stock pour le type de lait sélectionné !")

    def action_confirm(self):
        self._check_quantite_disponible()
        self.status = 'confirm'

    def action_done(self):
        self.status = 'done'

    def action_draft(self):
        self.status = 'draft'

    def action_cancel(self):
        self.status = 'cancel'
    @api.depends('type_lait')
    def _compute_quantite_en_stock(self):
      for record in self:
        total_quantity = sum(self.env['production.level'].search([('type_lait', '=', record.type_lait)]).mapped('quantite_en_stock_lait'))
        record.quantite_en_stock_lait = total_quantity
 
    def action_confirm(self):
        for record in self:
            if record.quantite_saisie > record.quantite_en_stock:
                raise UserError("La quantité saisie n'est pas disponible en stock pour le type de lait sélectionné !")
            level_records = self.env['production.level'].search([('type_lait', '=', record.type_lait)])
            for level_record in level_records:
                if level_record.quantite_en_stock_lait >= record.quantite_saisie:
                    level_record.quantite_en_stock_lait -= record.quantite_saisie
                    break
            else:
                raise UserError("La quantité saisie n'est pas disponible en stock pour le type de lait sélectionné !")
    @api.depends('quantite_saisie')
    def _compute_prix(self):
        for record in self:
          if record.quantite_saisie < 0:
            raise ValidationError("La quantité saisie ne peut pas être négative.")
        # Définir le prix unitaire directement dans la méthode
        prix_unitaire = 1 # Prix unitaire en euros
        record.prix = record.quantite_saisie * prix_unitaire
    @api.model
    def action_compute_prix(self):
     for record in self:
        record._compute_prix()
   


class ResPartner(models.Model):
    _inherit = 'res.partner'
class TechnicienAgricole(models.Model):
    _inherit = 'reproduction.technicien'
    _description = 'Technicien Agricole'
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    type_lait = fields.Selection([('vache', 'Lait de vache'), ('chèvre', 'Lait de chèvre')], string='Type de lait', required=True)
    quantite_en_stock_lait = fields.Float(string='Quantité en stock (litre)', compute='_compute_quantite_en_stock_lait', store=True)
    quantite_saisie = fields.Float(string='Quantité saisie (litre)', required=True)
    date_mouvement = fields.Date(string="Date de mouvement", default=fields.Date.today)
    prix = fields.Float(string='Prix', compute='_compute_prix', store=True)
   
    @api.constrains('quantite_saisie')
    def _check_quantite_disponible(self):
        for record in self:
            if record.quantite_saisie > record.quantite_en_stock_lait:
                raise UserError("La quantité saisie n'est pas disponible en stock pour le type de lait sélectionné !")
    @api.depends('type_lait')
    def _compute_quantite_en_stock_lait(self):
      for record in self:
        total_quantity = sum(self.env['production.level'].search([('type_lait', '=', record.type_lait)]).mapped('quantite_en_stock_lait'))
        record.quantite_en_stock_lait = total_quantity
    def action_confirm(self):
        for record in self:
            if record.quantite_saisie > record.quantite_en_stock_lait:
                raise UserError("La quantité saisie n'est pas disponible en stock pour le type de lait sélectionné !")
            level_records = self.env['production.level'].search([('type_lait', '=', record.type_lait)])
            for level_record in level_records:
                if level_record.quantite_en_stock_lait >= record.quantite_saisie:
                    level_record.quantite_en_stock_lait -= record.quantite_saisie
                    break
            else:
                raise UserError("La quantité saisie n'est pas disponible en stock pour le type de lait sélectionné !")
    @api.depends('quantite_saisie')
    def _compute_prix(self):
        for record in self:
          if record.quantite_saisie < 0:
            raise ValidationError("La quantité saisie ne peut pas être négative.")
        # Définir le prix unitaire directement dans la méthode
        prix_unitaire = 1 # Prix unitaire en euros
        record.prix = record.quantite_saisie * prix_unitaire
    @api.model
    def action_compute_prix(self):
     for record in self:
        record._compute_prix()
  


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

class ProjectTask(models.Model):
    _inherit = 'project.task'
  
    
    def create_task(self):
        # Exemple de création d'une tâche
        new_task_data = {
            'name': 'Nom de la tâche',
             # Utilise la date actuelle
            # Remplace technicien_id par l'ID du technicien
            # Remplace vache_id par l'ID de la vache
            # Remplace plante_id par l'ID de la plante
            # Autres champs à remplir
        }

        new_task = self.env['project.task'].create(new_task_data)

        # Exemple de mise à jour d'une tâche existante
        task_to_update = self.env['project.task'].browse([task_id])  # Remplace task_id par l'ID de la tâche à mettre à jour
        task_to_update.write({'date_planifiee': fields.Date.today()})  # Utilise la date actuelle pour la mise à jour


class ProductionAliment(models.Model):
    _name = 'production.aliment'
    _description = 'Stock des aliments'

    produit_reference = fields.Many2one('production.produit', string='Référence du produit')
    plante_id = fields.Many2one('production.plante', string='Plante')
   
    status = fields.Selection([('draft', 'Brouillon'), ('confirm', 'Confirmé'), ('done', 'Terminé')], string='Statut', default='draft')

  
