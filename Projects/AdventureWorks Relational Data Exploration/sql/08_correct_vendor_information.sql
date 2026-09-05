-- Task 3.2: Corrected vendor information query
SELECT
  vendor.VendorId AS vendor_id,
  vendor_contact.ContactId AS contact_id,
  vendor_contact.ContactTypeID AS contact_type_id,
  vendor.Name AS vendor_name,
  vendor.CreditRating AS credit_rating,
  vendor.ActiveFlag AS active_flag,
  vendor_address.AddressId AS address_id,
  address.City AS city
FROM `tc-da-1.adwentureworks_db.vendor` AS vendor
LEFT JOIN `tc-da-1.adwentureworks_db.vendorcontact` AS vendor_contact
  ON vendor.VendorId = vendor_contact.VendorId
LEFT JOIN `tc-da-1.adwentureworks_db.vendoraddress` AS vendor_address
  ON vendor.VendorId = vendor_address.VendorId
LEFT JOIN `tc-da-1.adwentureworks_db.address` AS address
  ON vendor_address.AddressId = address.AddressId;
