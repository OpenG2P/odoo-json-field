
from odoo import fields

from odoo import models, fields, api
from odoo.addons.g2p_encryption.models.crypto import AESCipher

class EncryptedPartner(models.Model):
    _inherit = "res.partner"

    # is_encrypted = fields.Boolean("Is encrypted?")
    
    name_decrypted = fields.Char(compute=lambda self:self._decrypt_field("name", "name_decrypted"), store=False)
    family_name_decrypted = fields.Char(compute=lambda self:self._decrypt_field("family_name", "family_name_decrypted"), store=False)
    given_name_decrypted = fields.Char(compute=lambda self:self._decrypt_field("given_name", "given_name_decrypted"), store=False)
    addl_name_decrypted = fields.Char(compute=lambda self:self._decrypt_field("addl_name", "addl_name_decrypted"), store=False)
    email_decrypted = fields.Char(compute=lambda self:self._decrypt_field("email", "email_decrypted"), store=False)
    phone_decrypted = fields.Char(compute=lambda self:self._decrypt_field("phone", "phone_decrypted"), store=False)
    mobile_decrypted = fields.Char(compute=lambda self:self._decrypt_field("mobile", "mobile_decrypted"), store=False)
    address_decrypted = fields.Char(compute=lambda self:self._decrypt_field("address", "address_decrypted"), store=False)
    birth_place_decrypted = fields.Char(compute=lambda self:self._decrypt_field("birth_place", "birth_place_decrypted"), store=False)



    @api.model
    def create(self, vals):
        record = super(EncryptedPartner, self).create(vals)
        #TODO encryption key should be moved to a secret vault.
        encryption_key = self.env['ir.config_parameter'].get_param('g2p_enc_key', '')
        if encryption_key:
            crypto = AESCipher(encryption_key)
            record["name"] = crypto.encrypt(record["name"]) if record["name"] else None
            record["family_name"] = crypto.encrypt(record["family_name"]) if record["family_name"] else None
            record["given_name"] = crypto.encrypt(record["given_name"]) if record["given_name"] else None
            record["addl_name"] = crypto.encrypt(record["addl_name"]) if record["addl_name"] else None
            record["display_name"] = crypto.encrypt(record["display_name"]) if record["display_name"] else None
            record["email"] = crypto.encrypt(record["email"]) if record["email"] else None
            record["phone"] = crypto.encrypt(record["phone"]) if record["phone"] else None
            record["mobile"] = crypto.encrypt(record["mobile"]) if record["mobile"] else None
            record["address"] = crypto.encrypt(record["address"]) if record["address"] else None
            record["birth_place"] = crypto.encrypt(record["birth_place"]) if record["birth_place"] else None

        return record
    

    def _decrypt_field(self,actual_field, decrypted_field) :
        #TODO encryption key should be moved to a secret vault.
        encryption_key = self.env['ir.config_parameter'].get_param('g2p_enc_key', '')
        if encryption_key:
            crypto = AESCipher(encryption_key)
            for rec in self:
                if rec[actual_field] :
                    rec[decrypted_field] = crypto.decrypt(rec[actual_field]) 
                else:
                    rec[decrypted_field] = ''
                print(decrypted_field,",",rec[decrypted_field])  
