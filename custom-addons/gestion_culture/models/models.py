from odoo import models, fields, api
from odoo import _


class Gestionculture(models.Model):
    _name = 'gestion_culture.gestion_culture'
    _description = 'Gestion des culture'

    name = fields.Char(string='Nom de la culture', required=True)
    farming_seasons = fields.Selection(
        [('hiver', 'Hiver'), ('printemps', 'Printemps'), ('ete', 'Été'), ('automne', 'Automne')],
        string='Saison de culture', required=True)
    emplacement = fields.Char(string='Emplacement')
    superficie = fields.Float(string='Superficie (ha)')
    agriculteur = fields.Many2one('res.partner', string='Agriculteur')
    image_couverture = fields.Binary(string='Image de couverture')

    etat = fields.Char('Etat', default='Recolté', readonly=True)

    def mon_bouton(self):
        if self.etat == 'Recolté':
            self.etat = 'non Recolté'
        else:
            self.etat = 'Recolté'
class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'
    
    bill_count = fields.Integer(string='Bill Count')

class Employee(models.Model):
    _inherit = 'hr.employee'

    # Ajoutez ici vos champs personnalisés pour les employés


class Parcelle(models.Model):
    _name = "gestion_culture.parcelle"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Parcelle"
 
    name = fields.Char(string='Nom de la culture', required=True)
    farming_seasons = fields.Selection(
        [('hiver', 'Hiver'), ('printemps', 'Printemps'), ('ete', 'Été'), ('automne', 'Automne')],
        string='Saison de culture', required=True)
    emplacement = fields.Char(string='Emplacement')
    superficie = fields.Float(string='Superficie (ha)')
    agriculteur = fields.Many2one('res.partner', string='Agriculteur')
    image = fields.Binary(string='Image')
    etat = fields.Selection([('en_cours', 'En cours'), ('recolte', 'Récolté')], string='Etat')
    name_seq = fields.Char(string="Order Reference", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        # Appeler la super méthode create pour créer l'enregistrement
        record = super(Parcelle, self).create(vals)

        # Mettre à jour le champ 'name_seq' pour chaque enregistrement créé
        for rec in record:
            rec.name_seq = self.env['ir.sequence'].next_by_code('culture.parcelle.sequence')

        # Retourner l'enregistrement créé
        return record  

    def mon_bouton(self):
        if self.etat == 'Recolté':
            self.etat = 'non Recolté'
        else:
            self.etat = 'Recolté'

    def action_save(self):
        # Votre logique pour enregistrer les données
        return True
  

class MaladieDetectee(models.Model):
    _name = 'gestion_culture.maladie_detectee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Maladie détectée'

    nom_maladie = fields.Char(string='Nom de la maladie')
    type_culture_affectee = fields.Char(string='Type de culture affectée')
    traitement_conseille = fields.Text(string='Traitement conseillé')
    image = fields.Binary(string='Image')
    date_detection = fields.Date(string='Date de détection')
    notes = fields.Text(string='Notes')
    symptomes = fields.Text(string='Symptômes')
    maladie_id = fields.Many2one('gestion_culture.maladie_detectee', string='Maladie')
    
    state = fields.Selection([
        ('draft', 'Non traitée'),
        ('done', 'Traitée'),
        ('cancel', 'Annulée'),
    ], default='draft', string="Status", required=True)
    name_seq = fields.Char(string="Order Reference", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
  
 
    
    @api.model
    def create(self, vals):
        # Appeler la super méthode create pour créer l'enregistrement
        record = super(MaladieDetectee, self).create(vals)

        # Mettre à jour le champ 'name_seq' pour chaque enregistrement créé
        for rec in record:
            rec.name_seq = self.env['ir.sequence'].next_by_code('culture.maladie.sequence')

        # Retourner l'enregistrement créé
        return record  

    def _process_attachments_for_post(self):
        attachments = self.env['ir.attachment'].search([('res_model', '=', self._name), ('res_id', '=', self.id)])
        attachment_ids = [(4, attachment.id) for attachment in attachments]
        return attachment_ids

    def action_edit_maladie(self):
        # Rediriger vers le formulaire d'édition de la maladie
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    @api.model
    def action_create_maladie(self):
        # Rediriger vers le formulaire de création d'une nouvelle maladie
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
        }



def send_email_template(self):
        template = self.env.ref('gestion_culture.maladie_detectee_mail_template')
        template.send_mail(self.id)


   
   

class MailTemplate(models.Model):
    _inherit = 'mail.template'

    res_model = fields.Char(string='Related Model', help='The model this template is related to')

    name = fields.Char(string='Nom')
    email_from = fields.Char(string='De')
    subject = fields.Char(string='Sujet')
    email_to = fields.Char(string='À')
    auto_delete = fields.Boolean(string='Suppression automatique')
    body_html = fields.Html(string='Corps HTML')
   

class Plante(models.Model):
    _name = 'gestion_culture.plante'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Plante'
   

    image = fields.Binary(string='Image')
    name = fields.Char(string='Nom')
    date = fields.Date(string='Date de plantation')
    date_prevue_recolte = fields.Date(string='Date prévue de récolte')
   
    type = fields.Selection([
    ('fruit', 'Fruit'),
    ('legume', 'Légume'),
    ('herbe', 'Herbe'),
    ('fleur', 'Fleur'),
], string='Type')

    longueur = fields.Float(string='Longueur (cm)', help='Longeueur en cm')
    largeur = fields.Float(string='Largeur')
    hauteur = fields.Float(string='Hauteur')
    quantite =  fields.Float('Quantité (Kilos)', help='Quantité en kilos')
    prix_unitaire = fields.Float(string='Prix unitaire')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    responsable_id = fields.Many2one('hr.employee', string='Responsable')
    statut = fields.Selection([('en_cours', 'En cours'), ('recolte', 'Récolté')], string='Statut')
    emplacement = fields.Char(string='Emplacement')
    parcelle=fields.Many2one('gestion_culture.parcelle', string='Parcelle')
    variation_longueur_ids = fields.One2many('gestion_culture.variation_longueur', 'plante_id', string='Variations de longueur')
    variation_quantite_ids = fields.One2many('gestion_culture.variation_quantite', 'plante_id', string='Variations de Quantite')
    name_seq = fields.Char(string="Order Reference", required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        record = super(Plante, self).create(vals)

        # Mettre à jour le champ 'name_seq' pour chaque enregistrement créé
        for rec in record:
            rec.name_seq = self.env['ir.sequence'].next_by_code('culture.Plante.sequence')

       
    # Ajoutez d'autres champs nécessaires pour le produit


            # Add other necessary fields for the product
    

        return record   

   
 
   
class VariationLongueur(models.Model):
    _name = 'gestion_culture.variation_longueur'

    plante_id = fields.Many2one('gestion_culture.plante', string='Plante')
    longueur = fields.Float('Longueur')
    date_du_jour = fields.Date(string="Date du jour", default=fields.Date.today)

    # Autres champs si nécessaire
class VariationQuantite(models.Model):
    _name = 'gestion_culture.variation_quantite'
    _description = 'Variations de Quantité'

    plante_id = fields.Many2one('gestion_culture.plante', string='Plante')
    quantite =  fields.Float('Quantité (Kilos)', help='Quantité en kilos')
    date_du_jour = fields.Date(string="Date du jour", default=fields.Date.today)